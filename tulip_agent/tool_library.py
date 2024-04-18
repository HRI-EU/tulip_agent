#!/usr/bin/env python3
"""
The tool library (tulip) for the agent
"""
import importlib
import json
import logging
import sys

import chromadb

from inspect import getmembers, isfunction
from os.path import dirname, abspath
from pathlib import Path
from typing import Callable, Optional

from .embed import embed
from .function_analyzer import FunctionAnalyzer


logger = logging.getLogger(__name__)


class ToolLibrary:
    def __init__(
        self,
        chroma_sub_dir: str = "",
        file_imports: list[tuple[str, Optional[list[str]]]] = None,
        chroma_base_dir: str = dirname(dirname(abspath(__file__))) + "/data/chroma/",
    ) -> None:
        self.function_analyzer = FunctionAnalyzer()
        self.functions = {}
        self.function_descriptions = {}
        self.function_origins = {}

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
            function_name = md["name"]
            identifier = md["identifier"]
            if identifier not in self.function_origins:
                self.function_origins[identifier] = {
                    "module_name": module_name,
                    "function_name": function_name,
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
            else:
                self.functions[identifier] = self.functions[identifier]

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
                logger.info(f"Embedding new functions: {new_functions}")
                self.collection.add(
                    documents=[
                        json.dumps(fd, indent=4)
                        for fd in new_function_descriptions.values()
                    ],
                    embeddings=[
                        embed(fd["function"]["description"])
                        for fd in new_function_descriptions.values()
                    ],
                    metadatas=[
                        {
                            "description": str(new_function_descriptions[f]),
                            "identifier": f,
                            "module": self.function_origins[f]["module_name"],
                            "name": self.function_origins[f]["function_name"],
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
    ) -> None:
        function_id = f"{module_name}__{function.__name__}"
        self.functions[function_id] = function
        function_data = self.function_analyzer.analyze_function(function)
        function_data["function"]["name"] = function_id
        self.function_descriptions[function_id] = function_data
        self.collection.add(
            documents=json.dumps(function_data, indent=4),
            embeddings=[embed(function_data["function"]["description"])],
            metadatas=[
                {
                    "description": str(function_data),
                    "identifier": function_id,
                    "module": module_name,
                    "name": function.__name__,
                }
            ],
            ids=[function_id],
        )
        self.function_origins[function_id] = {
            "module_name": module_name,
            "function_name": function.__name__,
        }
        logger.info(f"Added function {function_id} to collection {self.collection}.")

    def load_functions_from_file(
        self,
        module_name: str,
        function_names: Optional[list[str]] = None,
    ) -> None:
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
        for f in functions:
            self._add_function(function=f, module_name=module_name)

    def remove_function(
        self,
        function_id: str,
    ) -> None:
        self.collection.delete(ids=[function_id])
        self.functions.pop(function_id)
        self.function_descriptions.pop(function_id)
        logger.info(
            f"Removed function {function_id} from collection {self.collection}."
        )

    def search(
        self,
        problem_description: str,
        top_k: int = 1,
        similarity_threshold: float = None,
    ):
        query_embedding = embed(problem_description)
        res = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "distances"],
        )
        return res

    def execute(
        self,
        function_id: str,
        function_args: dict,
    ):
        try:
            res = self.functions[function_id](**function_args)
        except Exception as e:
            logger.error(e)
            res = f"Invalid tool call for {function_id}. Continue without this information."
        return res
