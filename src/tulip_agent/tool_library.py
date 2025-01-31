#!/usr/bin/env python3
#
# Copyright (c) 2024, Honda Research Institute Europe GmbH
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""
The tool library (tulip) for the agent
"""
import importlib
import json
import logging
import sys
from inspect import getmembers, isfunction
from os.path import abspath, dirname
from pathlib import Path
from typing import Callable, Optional

import chromadb

from tulip_agent.client_setup import ModelServeMode, create_client
from tulip_agent.constants import BASE_EMBEDDING_MODEL
from tulip_agent.embed import embed
from tulip_agent.function_analyzer import FunctionAnalyzer
from tulip_agent.tool import Tool


logger = logging.getLogger(__name__)


class ToolLibrary:
    def __init__(
        self,
        chroma_sub_dir: str = "",
        file_imports: Optional[list[tuple[str, Optional[list[str]]]]] = None,
        instance_imports: Optional[list[object]] = None,
        chroma_base_dir: str = dirname(dirname(dirname(abspath(__file__))))
        + "/data/chroma/",
        embedding_model: str = BASE_EMBEDDING_MODEL,
        model_serve_mode: ModelServeMode = ModelServeMode.OPENAI,
        description: Optional[str] = None,
        default_timeout: int = 60,
        default_timeout_message: str = (
            "Error: The tool did not return a response within the specified timeout."
        ),
        timeout_settings: Optional[dict] = None,
    ) -> None:
        """
        Initialize the tool library: set up the vector store and load the tool information.

        :param chroma_sub_dir: A specific subfolder for the tool library.
        :param file_imports: List of tuples with a module name from which to load tools from and
            an optional list of tools to load. If no tools are specified, all tools are loaded.
        :param instance_imports: List of instances of classes from which to load tools.
        :param chroma_base_dir: Absolute path to the tool library folder.
        :param embedding_model: Name of the embedding model used. Defaults to the one specified in constants.
        :param model_serve_mode: Model serving mode. Defaults to OPENAI.
        :param description: Natural language description of the tool library.
        :param default_timeout: Execution timeout for tools.
        :param default_timeout_message: Default message returned in case of tool execution timeout.
        :param timeout_settings: Tool-specific timeout settings of the form
            {"module_name__tool_name": {"timeout": seconds, "timeout_message": string}}
            NOTE: overriding existing timeout settings is not supported
        """
        self.description = description
        self.embedding_model = embedding_model
        self.embedding_client = create_client(model_serve_mode)

        self.function_analyzer = FunctionAnalyzer()
        self.tools: dict[str, Tool] = {}

        # timeout settings
        self.default_timeout = default_timeout
        self.default_timeout_message = default_timeout_message
        timeout_settings = timeout_settings if timeout_settings else {}

        # set up directory
        chroma_dir = chroma_base_dir + chroma_sub_dir
        Path(chroma_dir).mkdir(parents=True, exist_ok=True)

        # vector store
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = self.chroma_client.get_or_create_collection(name="tulip")
        stored_tools = self.collection.get(include=["metadatas"])
        stored_tools_ids = stored_tools["ids"]

        # load functions available in vector store
        for metadata in stored_tools["metadatas"]:
            # TODO: check that files and instances are actually supposed to be provided
            if metadata["class_name"]:
                continue
            tool = Tool(
                function_name=metadata["function_name"],
                module_name=metadata["module_name"],
                definition=json.loads(metadata["definition"]),
                timeout=metadata["timeout"],
                timeout_message=metadata["timeout_message"],
                predecessor=(
                    metadata["predecessor"] if "predecessor" in metadata else None
                ),
                successor=metadata["successor"] if "successor" in metadata else None,
            )
            self.tools[tool.unique_id] = tool

        # load tools from files and instances
        if not file_imports and not instance_imports:
            return
        file_imports = file_imports if file_imports else []
        for file_import in file_imports:
            module_name, function_names = file_import
            module = importlib.import_module(module_name)
            functions = [
                f
                for n, f in getmembers(module, isfunction)
                if f.__module__ == module_name
                and (not function_names or n in function_names)
            ]
            for function in functions:
                function_definition = self.function_analyzer.analyze_function(function)
                tool = Tool(
                    function_name=function.__name__,
                    module_name=module_name,
                    definition=function_definition,
                    timeout=self.default_timeout,
                    timeout_message=self.default_timeout_message,
                )
                if tool.unique_id in timeout_settings:
                    tool.timeout = timeout_settings[tool.unique_id]["timeout"]
                    tool.timeout_message = timeout_settings[tool.unique_id][
                        "timeout_message"
                    ]
                self.tools[tool.unique_id] = tool
        instance_imports = instance_imports if instance_imports else []
        for instance_import in instance_imports:
            function_definitions = self.function_analyzer.analyze_class(
                instance_import.__class__
            )
            for function_definition in function_definitions:
                tool = Tool(
                    function_name=function_definition["function"]["name"],
                    module_name=instance_import.__module__,
                    instance=instance_import,
                    definition=function_definition,
                    timeout=self.default_timeout,
                    timeout_message=self.default_timeout_message,
                )
                if tool.unique_id in timeout_settings:
                    tool.timeout = timeout_settings[tool.unique_id]["timeout"]
                    tool.timeout_message = timeout_settings[tool.unique_id][
                        "timeout_message"
                    ]
                self.tools[tool.unique_id] = tool

        # load new functions into vector store
        new_tools = [
            tool
            for tool_id, tool in self.tools.items()
            if tool_id not in stored_tools_ids
        ]
        if not new_tools:
            return
        self._save_to_vector_store(new_tools)

    def _save_to_vector_store(self, tools: list[Tool]) -> None:
        tool_lookup = {tool.unique_id: tool for tool in tools}
        logger.info(
            f"Adding tools to collection {self.collection}: {tool_lookup.keys()}"
        )
        self.collection.add(
            documents=[
                json.dumps(tool.definition, indent=4) for tool in tool_lookup.values()
            ],
            embeddings=[
                embed(
                    text=tool.description,
                    embedding_client=self.embedding_client,
                    embedding_model=self.embedding_model,
                )
                for tool in tool_lookup.values()
            ],
            metadatas=[tool.format_for_chroma() for tool in tool_lookup.values()],
            ids=list(tool_lookup.keys()),
        )

    def _add_function(
        self,
        function: Callable,
        module_name: str,
        timeout: Optional[int] = None,
        timeout_message: Optional[str] = None,
    ) -> Tool:
        function_definition = self.function_analyzer.analyze_function(function)
        tool = Tool(
            function_name=function.__name__,
            module_name=module_name,
            definition=function_definition,
            timeout=timeout if timeout is not None else self.default_timeout,
            timeout_message=(
                timeout_message
                if timeout_message is not None
                else self.default_timeout_message
            ),
        )
        self.tools[tool.unique_id] = tool
        self._save_to_vector_store(tools=[tool])
        return tool

    def load_functions_from_file(
        self,
        module_name: str,
        function_names: Optional[list[str]] = None,
        timeout_settings: Optional[dict] = None,
    ) -> list[Tool]:
        timeout_settings = timeout_settings if timeout_settings else {}
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)
        functions = [
            f
            for n, f in getmembers(module, isfunction)
            if f.__module__ == module_name
            and (not function_names or n in function_names)
        ]
        tools = []
        for function in functions:
            tool_id = f"{module_name}__{function.__name__}"
            timeout_settings_ = (
                timeout_settings[tool_id] if tool_id in timeout_settings else {}
            )
            tool = self._add_function(
                function=function,
                module_name=module_name,
                **timeout_settings_,
            )
            tools.append(tool)
        return tools

    def load_functions_from_instance(
        self, instance: object, timeout_settings: Optional[dict] = None
    ) -> list[Tool]:
        timeout_settings = timeout_settings if timeout_settings else {}
        function_definitions = self.function_analyzer.analyze_class(instance.__class__)
        new_tools = []
        for function_definition in function_definitions:
            tool = Tool(
                function_name=function_definition["function"]["name"],
                module_name=instance.__module__,
                instance=instance,
                definition=function_definition,
                timeout=self.default_timeout,
                timeout_message=self.default_timeout_message,
            )
            if tool.unique_id in timeout_settings:
                tool.timeout = timeout_settings[tool.unique_id]["timeout"]
                tool.timeout_message = timeout_settings[tool.unique_id][
                    "timeout_message"
                ]
            new_tools.append(tool)
            self.tools[tool.unique_id] = tool

        self._save_to_vector_store(tools=new_tools)
        return new_tools

    def remove_tool(
        self,
        tool_id: str,
    ) -> None:
        self.collection.delete(ids=[tool_id])
        self.tools.pop(tool_id)
        logger.info(f"Removed tool {tool_id} from collection {self.collection}.")

    def update_tool(
        self,
        tool_id: str,
        timeout: Optional[int] = None,
        timeout_message: Optional[str] = None,
    ) -> Tool:
        old_tool = self.tools[tool_id]
        module_name = old_tool.module_name
        timeout = timeout or old_tool.timeout
        timeout_message = timeout_message or old_tool.timeout_message

        module_occurrences = len(
            [t for t in self.tools.values() if t.module_name == module_name]
        )
        if module_occurrences != 1:
            raise ValueError(
                f"Update operation is only supported for modules with exactly one function. "
                f"{module_name} includes {module_occurrences}."
            )

        module = importlib.reload(old_tool.module)
        function = getattr(module, old_tool.function_name)

        self.remove_tool(tool_id)
        tool = self._add_function(
            function=function,
            module_name=module.__name__,
            timeout=timeout,
            timeout_message=timeout_message,
        )
        return tool

    def search(
        self,
        problem_description: str,
        top_k: int = 1,
        similarity_threshold: float = None,
    ) -> list[Tool]:
        if top_k >= len(self.tools) and similarity_threshold is None:
            res = self.tools.values()
        else:
            query_embedding = embed(
                text=problem_description,
                embedding_client=self.embedding_client,
                embedding_model=self.embedding_model,
            )
            res = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["distances"],
            )
            cutoff = top_k
            if similarity_threshold:
                for c, distance in enumerate(res["distances"][0]):
                    if distance >= similarity_threshold:
                        cutoff = c
                        break
            res = [self.tools[tool_id] for tool_id in res["ids"][0][:cutoff]]
        return res

    def execute(
        self,
        tool_id: str,
        arguments: dict,
    ) -> tuple:
        if tool_id not in self.tools:
            return (
                f"Error: {tool_id} is not a valid tool. Use only the tools available.",
                True,
            )
        tool = self.tools[tool_id]
        return tool.execute(**arguments)
