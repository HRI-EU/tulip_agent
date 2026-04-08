#!/usr/bin/env python3
#
#  Copyright (c) 2024-2025, Honda Research Institute Europe GmbH
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  SPDX-License-Identifier: BSD-3-Clause
#
#
from __future__ import annotations

import asyncio
import atexit
import importlib
import inspect
import json
import logging
import os
import sys
import threading
from abc import ABC
from dataclasses import asdict, dataclass, field
from types import ModuleType
from typing import Any, Callable, Optional

from fastmcp import Client


logger = logging.getLogger(__name__)


class McpClientManager:
    """Manages persistent MCP client connections, one per unique server config."""

    def __init__(self):
        self._clients: dict[str, Client] = {}
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        atexit.register(self._shutdown)

    def _ensure_loop(self):
        if self._loop is None or self._loop.is_closed():
            self._loop = asyncio.new_event_loop()
            self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
            self._thread.start()

    async def _get_client(self, config_key: str, mcp_config: dict) -> Client:
        if config_key not in self._clients:
            client = Client(mcp_config)
            await client.__aenter__()
            self._clients[config_key] = client
        return self._clients[config_key]

    def call_tool(
        self, config_key: str, mcp_config: dict, function_name: str, parameters: dict
    ):
        self._ensure_loop()
        return asyncio.run_coroutine_threadsafe(
            self._call(config_key, mcp_config, function_name, parameters), self._loop
        ).result()

    async def _call(self, config_key, mcp_config, function_name, parameters):
        client = await self._get_client(config_key, mcp_config)
        res = await client.call_tool(function_name, parameters)
        return res.content[0].text

    def list_tools(self, config_key: str, mcp_config: dict):
        self._ensure_loop()
        return asyncio.run_coroutine_threadsafe(
            self._list_tools(config_key, mcp_config), self._loop
        ).result()

    async def _list_tools(self, config_key, mcp_config):
        client = await self._get_client(config_key, mcp_config)
        return await client.list_tools()

    async def _close_all(self):
        for config_key, client in self._clients.items():
            try:
                await client.__aexit__(None, None, None)
            except (OSError, asyncio.CancelledError):
                logger.debug(
                    "MCP client %s already closed during shutdown.", config_key
                )
        self._clients.clear()

    def _shutdown(self):
        if self._loop is None or self._loop.is_closed():
            return
        asyncio.run_coroutine_threadsafe(self._close_all(), self._loop).result(
            timeout=5
        )
        self._loop.call_soon_threadsafe(self._loop.stop)


@dataclass(eq=False)
class Tool(ABC):
    function_name: str
    definition: dict
    unique_id: str = field(init=False)
    module_path: str = field(init=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object {id(self)}: {self.unique_id}>"

    def __call__(self, **parameters) -> str:
        return self.function(**parameters)

    def format_for_chroma(self) -> dict:
        raise NotImplementedError


@dataclass(eq=False)
class ImportedTool(Tool):
    module_name: Optional[str] = None
    instance: Optional[object] = None
    function: Optional[Callable] = None
    class_name: str = ""
    timeout: Optional[float] = None
    timeout_message: Optional[str] = None
    predecessor: Optional[str] = None
    successor: Optional[str] = None
    verbose_id: bool = False
    description: str = field(init=False)

    @classmethod
    def from_function(
        cls,
        function: Callable,
        definition: dict,
        timeout: Optional[float] = None,
        timeout_message: Optional[str] = None,
        verbose_id: bool = False,
    ) -> ImportedTool:
        return cls(
            function_name=function.__name__,
            definition=definition,
            function=function,
            timeout=timeout,
            timeout_message=timeout_message,
            verbose_id=verbose_id,
        )

    @classmethod
    def from_module(
        cls,
        module_name: str,
        function_name: str,
        definition: dict,
        instance: Optional[object] = None,
        timeout: Optional[float] = None,
        timeout_message: Optional[str] = None,
        predecessor: Optional[str] = None,
        successor: Optional[str] = None,
        verbose_id: bool = False,
    ) -> ImportedTool:
        return cls(
            function_name=function_name,
            module_name=module_name,
            definition=definition,
            instance=instance,
            timeout=timeout,
            timeout_message=timeout_message,
            predecessor=predecessor,
            successor=successor,
            verbose_id=verbose_id,
        )

    def __post_init__(self) -> None:
        if self.function is not None:
            module = inspect.getmodule(self.function)
            self.module_name = module.__name__ if module else "__main__"
            module_path = inspect.getsourcefile(self.function)
            self.module_path = os.path.abspath(module_path) if module_path else ""
            clean_module_name = self.module_name.replace(".", "__")
            if self.verbose_id:
                self.unique_id = f"{clean_module_name}__{self.function_name}"
            else:
                self.unique_id = self.function_name
        else:
            if not self.module_name:
                raise ValueError(
                    "ImportedTool requires either `function` or `module_name`."
                )
            self.module: ModuleType = (
                sys.modules[self.module_name]
                if self.module_name in sys.modules
                else importlib.import_module(self.module_name)
            )
            self.module_path = os.path.abspath(self.module.__file__)
            clean_module_name = self.module_name.replace(".", "__")
            if self.instance:
                if self.verbose_id:
                    self.unique_id = f"{clean_module_name}__{self.instance.__class__.__name__}__{self.function_name}"
                else:
                    self.unique_id = self.function_name
                self.function = getattr(self.instance, self.function_name)
                self.class_name = self.instance.__class__.__name__
            else:
                if self.verbose_id:
                    self.unique_id = f"{clean_module_name}__{self.function_name}"
                else:
                    self.unique_id = self.function_name
                self.function = getattr(self.module, self.function_name)

        if self.instance and self.function is not None and self.class_name == "":
            if self.verbose_id:
                clean_module_name = self.module_name.replace(".", "__")
                self.unique_id = f"{clean_module_name}__{self.instance.__class__.__name__}__{self.function_name}"
            self.class_name = self.instance.__class__.__name__
        self.description = (
            self.function_name + ":\n" + self.definition["function"]["description"]
        )
        self.definition["function"]["name"] = self.unique_id

    def format_for_chroma(self) -> dict:
        flat_dict = asdict(self)
        flat_dict["tool_type"] = "imported"
        flat_dict["definition"] = json.dumps(self.definition, indent=4)
        if self.predecessor is None:
            flat_dict.pop("predecessor")
        if self.successor is None:
            flat_dict.pop("successor")
        flat_dict.pop("instance")
        flat_dict.pop("function")
        return flat_dict


@dataclass(eq=False)
class InternalTool(Tool):
    function: Callable
    timeout: Optional[float] = None
    timeout_message: Optional[str] = None
    verbose_id: bool = False

    def __post_init__(self) -> None:
        self.module_path = os.path.abspath(self.function.__func__.__code__.co_filename)
        if self.verbose_id:
            clean_module_name = self.function.__func__.__module__.replace(".", "__")
            self.unique_id = f"{clean_module_name}__{self.function_name}"
        else:
            self.unique_id = self.function_name
        self.definition["function"]["name"] = self.unique_id


@dataclass(eq=False)
class McpTool(Tool):
    mcp_config: dict[str, Any]
    mcp_manager: McpClientManager
    timeout: Optional[float] = None
    timeout_message: Optional[str] = None
    verbose_id: bool = False

    @classmethod
    def serialized_config(cls, mcp_config: dict[str, Any]) -> str:
        return json.dumps(mcp_config, sort_keys=True, separators=(",", ":"))

    @classmethod
    def config_from_metadata(cls, metadata: dict[str, Any]) -> dict[str, Any]:
        if "mcp_config" not in metadata:
            raise ValueError(
                "Stored MCP metadata is missing required `mcp_config` for "
                f"{metadata.get('unique_id', '<unknown>')}."
            )
        return json.loads(metadata["mcp_config"])

    def __post_init__(self) -> None:
        self.module_path = self.serialized_config(self.mcp_config)
        if self.verbose_id:
            clean_module_name = "mcp_config"
            self.unique_id = f"{clean_module_name}__{self.function_name}"
        else:
            self.unique_id = self.function_name
        self.description = (
            self.function_name + ":\n" + self.definition["function"]["description"]
        )
        self.definition["function"]["name"] = self.unique_id

    def __call__(self, **parameters):
        return self.mcp_manager.call_tool(
            self.module_path, self.mcp_config, self.function_name, parameters
        )

    def format_for_chroma(self) -> dict:
        return {
            "tool_type": "mcp",
            "unique_id": self.unique_id,
            "function_name": self.function_name,
            "definition": json.dumps(self.definition, indent=4),
            "mcp_config": self.serialized_config(self.mcp_config),
            "timeout": self.timeout,
            "timeout_message": self.timeout_message,
        }
