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
from __future__ import annotations

import concurrent.futures
import importlib
import json
import logging
import sys

from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Optional
from types import ModuleType


logger = logging.getLogger(__name__)


@dataclass(eq=False)
class Tool:
    function_name: str
    module_name: str
    definition: dict
    timeout: Optional[int] = None
    timeout_message: Optional[str] = None
    predecessor: Optional[str] = None
    successor: Optional[str] = None
    description: str = field(init=False)
    unique_id: str = field(init=False)

    def __post_init__(self) -> None:
        self.unique_id = f"{self.module_name}__{self.function_name}"
        self.description = (
            self.function_name + ":\n" + self.definition["function"]["description"]
        )
        self.definition["function"]["name"] = self.unique_id
        self.module: ModuleType = (
            sys.modules[self.module_name]
            if self.module_name in sys.modules
            else importlib.import_module(self.module_name)
        )
        self.function: Callable = getattr(self.module, self.function_name)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object {id(self)}: {self.unique_id}>"

    def format_for_chroma(self) -> dict:
        flat_dict = asdict(self)
        flat_dict["definition"] = json.dumps(self.definition, indent=4)
        return flat_dict

    def execute(self, **parameters) -> Any:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                future = executor.submit(self.function, **parameters)
            except Exception as e:
                logger.error(f"{type(e).__name__}: {e}")
                return f"Error: Invalid tool call for {self.unique_id}: {e}", True
            try:
                res = future.result(timeout=self.timeout)
                error = False
            except concurrent.futures.TimeoutError as e:
                logger.error(
                    f"{type(e).__name__}: {self.unique_id} did not return a result before timeout."
                )
                return self.timeout_message, True
            except Exception as e:
                logger.error(f"{type(e).__name__}: {e}")
                return f"Error: Invalid tool call for {self.unique_id}: {e}", True
        return res, error
