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

import importlib
import inspect
import json
import logging
import os
import sys
from abc import ABC
from dataclasses import asdict, dataclass, field
from types import ModuleType
from typing import Callable, Optional


logger = logging.getLogger(__name__)


@dataclass(eq=False)
class Tool(ABC):
    function_name: str
    definition: dict
    unique_id: str = field(init=False)
    module_path: str = field(init=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object {id(self)}: {self.unique_id}>"

    def execute(self, **parameters) -> str:
        return self.function(**parameters)


@dataclass(eq=False)
class ImportedTool(Tool):
    module_name: str
    instance: Optional[object] = None
    class_name: str = ""
    timeout: Optional[float] = None
    timeout_message: Optional[str] = None
    predecessor: Optional[str] = None
    successor: Optional[str] = None
    verbose_id: bool = False
    description: str = field(init=False)

    def __post_init__(self) -> None:
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
            self.function: Callable = getattr(self.instance, self.function_name)
            self.class_name = self.instance.__class__.__name__
        else:
            if self.verbose_id:
                self.unique_id = f"{clean_module_name}__{self.function_name}"
            else:
                self.unique_id = self.function_name
            self.function: Callable = getattr(self.module, self.function_name)
        self.description = (
            self.function_name + ":\n" + self.definition["function"]["description"]
        )
        self.definition["function"]["name"] = self.unique_id

    def format_for_chroma(self) -> dict:
        flat_dict = asdict(self)
        flat_dict["definition"] = json.dumps(self.definition, indent=4)
        if self.predecessor is None:
            flat_dict.pop("predecessor")
        if self.successor is None:
            flat_dict.pop("successor")
        flat_dict.pop("instance")
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
class ExternalTool(Tool):
    function: Callable
    timeout: Optional[float] = None
    timeout_message: Optional[str] = None
    verbose_id: bool = False

    def __post_init__(self) -> None:
        self.module_path = os.path.abspath(inspect.getsourcefile(self.function))
        if self.verbose_id:
            clean_module_name = inspect.getmodule(self.function).__name__.replace(
                ".", "__"
            )
            self.unique_id = f"{clean_module_name}__{self.function_name}"
        else:
            self.unique_id = self.function_name
        self.definition["function"]["name"] = self.unique_id
