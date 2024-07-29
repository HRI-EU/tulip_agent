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
import concurrent.futures
import importlib
import json
import logging
import os
import sys
from inspect import getmembers, isfunction
from os.path import abspath, dirname
from pathlib import Path
from typing import Callable, Optional

import chromadb

from .constants import BASE_EMBEDDING_MODEL
from .embed import embed
from .function_analyzer import FunctionAnalyzer


logger = logging.getLogger(__name__)


class ToolLibrary:
    def __init__(
        self,
        chroma_sub_dir: str = "",
        file_imports: list[tuple[str, Optional[list[str]]]] = None,
        chroma_base_dir: str = dirname(dirname(dirname(abspath(__file__))))
        + "/data/chroma/",
        embedding_model: str = BASE_EMBEDDING_MODEL,
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
        :param chroma_base_dir: Absolute path to the tool library folder.
        :param embedding_model: Name of the embedding model used. Defaults to the one specified in constants.
        :param description: Natural language description of the tool library.
        :param default_timeout: Execution timeout for tools.
        :param default_timeout_message: Default message returned in case of tool execution timeout.
        :param timeout_settings: Tool-specific timeout settings of the form
            {"module_name__tool_name": {"timeout": seconds, "timeout_message": string}}
            NOTE: overriding existing timeout settings is not supported
        """
        self.description = description
        self.embedding_model = embedding_model

        self.function_analyzer = FunctionAnalyzer()
        self.functions = {}
        self.function_descriptions = {}
        self.function_origins = {}

        # timeout settings
        self.default_timeout = default_timeout
        self.default_timeout_message = default_timeout_message
        self.timeout_settings = timeout_settings if timeout_settings else {}

        # import tools from file
        if file_imports:
            for file_import in file_imports:
                module_name, function_names = file_import
                module = importlib.import_module(module_name)
                if function_names:
                    functions_ = [
                        f
                        for n, f in getmembers(module, isfunction)
                        if f.__module__ == module_name and n in function_names
                    ]
                else:
                    functions_ = [
                        f
                        for _, f in getmembers(module, isfunction)
                        if f.__module__ == module_name
                    ]
                for f_ in functions_:
                    function_id = f"{module_name}__{f_.__name__}"
                    self.functions[function_id] = f_
                    f_description = self.function_analyzer.analyze_function(f_)
                    f_description["function"]["name"] = function_id
                    self.function_descriptions[function_id] = f_description
                    self.function_origins[function_id] = {
                        "module_name": module_name,
                        "function_name": f_.__name__,
                        "module_path": os.path.abspath(module.__file__),
                    }

        # set up directory
        chroma_dir = chroma_base_dir + chroma_sub_dir
        Path(chroma_dir).mkdir(parents=True, exist_ok=True)

        # vector store
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = self.chroma_client.get_or_create_collection(name="tulip")
        loaded_functions = self.collection.get(include=["metadatas"])
        loaded_functions_ids = loaded_functions["ids"]

        # load functions available in vector store
        for md in loaded_functions["metadatas"]:
            module_name = md["module"]
            module_path = md["path"]
            function_name = md["name"]
            identifier = md["identifier"]
            timeout = md["timeout"]
            timeout_message = md["timeout_message"]
            if identifier not in self.function_origins:
                self.function_origins[identifier] = {
                    "module_name": module_name,
                    "function_name": function_name,
                    "module_path": module_path,
                }
            if module_name:
                if module_name not in sys.modules:
                    try:
                        module = importlib.import_module(module_name)
                    except ModuleNotFoundError:
                        logger.error(f"No module found for {module_name}.")
                        self.remove_function(identifier)
                        continue
                else:
                    module = sys.modules[module_name]
                try:
                    self.functions[identifier] = getattr(module, function_name)
                except AttributeError:
                    logger.error(
                        f"No function found for {function_name} in {module_name}."
                    )
                    self.remove_function(identifier)
                    continue
            self.timeout_settings[identifier] = {
                "timeout": timeout,
                "timeout_message": timeout_message,
            }

        # load new functions into vector store
        if self.functions:
            new_functions = {
                n: d for n, d in self.functions.items() if n not in loaded_functions_ids
            }
            new_function_descriptions = {
                n: d
                for n, d in self.function_descriptions.items()
                if n not in loaded_functions_ids
            }
            if new_functions:
                for f in new_function_descriptions:
                    if f not in self.timeout_settings:
                        self.timeout_settings[f] = {
                            "timeout": self.default_timeout,
                            "timeout_message": self.default_timeout_message,
                        }
                logger.info(f"Embedding new functions: {new_functions}")
                self.collection.add(
                    documents=[
                        json.dumps(fd, indent=4)
                        for fd in new_function_descriptions.values()
                    ],
                    embeddings=[
                        embed(
                            text=self.functions[fd["function"]["name"]].__name__
                            + ":\n"
                            + fd["function"]["description"],
                            embedding_model=self.embedding_model,
                        )
                        for fd in new_function_descriptions.values()
                    ],
                    metadatas=[
                        {
                            "description": str(new_function_descriptions[f]),
                            "identifier": f,
                            "module": self.function_origins[f]["module_name"],
                            "path": self.function_origins[f]["module_path"],
                            "name": self.function_origins[f]["function_name"],
                            "timeout": self.timeout_settings[f]["timeout"],
                            "timeout_message": self.timeout_settings[f][
                                "timeout_message"
                            ],
                        }
                        for f in new_function_descriptions
                    ],
                    ids=[
                        val["function"]["name"]
                        for fd, val in new_function_descriptions.items()
                    ],
                )

    def _add_function(
        self,
        function: Callable,
        module_name: str,
        timeout: int = None,
        timeout_message: str = None,
    ) -> dict:
        module_path = os.path.abspath(sys.modules[module_name].__file__)
        function_id = f"{module_name}__{function.__name__}"
        self.functions[function_id] = function
        function_data = self.function_analyzer.analyze_function(function)
        function_data["function"]["name"] = function_id
        self.function_descriptions[function_id] = function_data

        self.timeout_settings[function_id] = {
            "timeout": timeout if timeout is not None else self.default_timeout,
            "timeout_message": (
                timeout_message
                if timeout_message is not None
                else self.default_timeout_message
            ),
        }

        self.collection.add(
            documents=json.dumps(function_data, indent=4),
            embeddings=[
                embed(
                    text=function.__name__
                    + ":\n"
                    + function_data["function"]["description"],
                    embedding_model=self.embedding_model,
                )
            ],
            metadatas=[
                {
                    "description": str(function_data),
                    "identifier": function_id,
                    "module": module_name,
                    "path": module_path,
                    "name": function.__name__,
                    "timeout": self.timeout_settings[function_id]["timeout"],
                    "timeout_message": self.timeout_settings[function_id][
                        "timeout_message"
                    ],
                }
            ],
            ids=[function_id],
        )

        self.function_origins[function_id] = {
            "module_name": module_name,
            "module_path": module_path,
            "function_name": function.__name__,
        }

        logger.info(f"Added function {function_id} to collection {self.collection}.")
        return function_data

    def load_functions_from_file(
        self,
        module_name: str,
        function_names: Optional[list[str]] = None,
        timeout_settings: dict = None,
    ) -> list[dict]:
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)
        if function_names:
            functions = [
                f
                for n, f in getmembers(module, isfunction)
                if f.__module__ == module_name and n in function_names
            ]
        else:
            functions = [
                f
                for _, f in getmembers(module, isfunction)
                if f.__module__ == module_name
            ]
        tool_descriptions = []
        timeout_settings = timeout_settings or {}
        for f in functions:
            timeout = (
                timeout_settings[f.__name__]["timeout"]
                if f.__name__ in timeout_settings
                else self.default_timeout
            )
            timeout_message = (
                timeout_settings[f.__name__]["timeout_message"]
                if f.__name__ in timeout_settings
                else self.default_timeout_message
            )
            tool_description = self._add_function(
                function=f,
                module_name=module_name,
                timeout=timeout,
                timeout_message=timeout_message,
            )
            tool_descriptions.append(tool_description)
        return tool_descriptions

    def remove_function(
        self,
        function_id: str,
    ) -> None:
        self.collection.delete(ids=[function_id])
        self.functions.pop(function_id)
        self.function_descriptions.pop(function_id)
        self.timeout_settings.pop(function_id)
        logger.info(
            f"Removed function {function_id} from collection {self.collection}."
        )

    def update_function(
        self,
        function_id: str,
        timeout: int = None,
        timeout_message: str = None,
    ) -> dict:
        module_name = self.function_origins[function_id]["module_name"]
        module = sys.modules[module_name]
        function_name = self.function_origins[function_id]["function_name"]
        timeout = timeout if timeout else self.timeout_settings[function_id]["timeout"]
        timeout_message = (
            timeout_message
            if timeout_message
            else self.timeout_settings[function_id]["timeout_message"]
        )

        module_occurrences = len(
            [
                e
                for e in self.function_origins
                if self.function_origins[e]["module_name"] == module_name
            ]
        )
        if module_occurrences != 1:
            raise ValueError(
                f"Update operation is only supported for modules with exactly one function. "
                f"{module_name} includes {module_occurrences}."
            )

        module = importlib.reload(module)
        f_ = getattr(module, function_name)

        self.remove_function(function_id)
        function_data = self._add_function(
            function=f_,
            module_name=module.__name__,
            timeout=timeout,
            timeout_message=timeout_message,
        )
        return function_data

    def search(
        self,
        problem_description: str,
        top_k: int = 1,
        similarity_threshold: float = None,
    ):
        query_embedding = embed(
            text=problem_description, embedding_model=self.embedding_model
        )
        res = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["distances", "documents", "metadatas"],
        )
        cutoff = top_k
        if similarity_threshold:
            for c, distance in enumerate(res["distances"][0]):
                if distance >= similarity_threshold:
                    cutoff = c
                    break
        res = {
            "ids": [res["ids"][0][:cutoff]],
            "distances": [res["distances"][0][:cutoff]],
            "documents": [res["documents"][0][:cutoff]],
            "metadatas": [res["metadatas"][0][:cutoff]],
        }
        return res

    def execute(
        self,
        function_id: str,
        function_args: dict,
    ) -> tuple:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                future = executor.submit(self.functions[function_id], **function_args)
            except KeyError as e:
                logger.error(f"{type(e).__name__}: {e}")
                return (
                    f"Error: {function_id} is not a valid tool. Use only the tools available.",
                    True,
                )
            except Exception as e:
                logger.error(f"{type(e).__name__}: {e}")
                return f"Error: Invalid tool call for {function_id}: {e}", True
            try:
                res = future.result(
                    timeout=self.timeout_settings[function_id]["timeout"]
                )
                error = False
            except concurrent.futures.TimeoutError as e:
                logger.error(
                    f"{type(e).__name__}: {function_id} did not return a result before timeout."
                )
                return self.timeout_settings[function_id]["timeout_message"], True
            except Exception as e:
                logger.error(f"{type(e).__name__}: {e}")
                return f"Error: Invalid tool call for {function_id}: {e}", True
        return res, error
