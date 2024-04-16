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
from pathlib import Path

from .embed import embed
from .function_analyzer import FunctionAnalyzer


logger = logging.getLogger(__name__)


class ToolLibrary:
    def __init__(
        self,
        chroma_sub_dir: str = "",
        functions: list = None,
        file_imports: list[tuple[str, list[str]]] = None,
        chroma_base_dir: str = "../data/chroma/",
    ) -> None:
        self.function_analyzer = FunctionAnalyzer()
        self.functions = {f.__name__: f for f in functions} if functions else {}
        self.function_descriptions = (
            {f.__name__: self.function_analyzer.analyze_function(f) for f in functions}
            if functions
            else {}
        )

        # import tools from file
        self.file_imports = file_imports if file_imports else []
        self.function_origins = {}
        if file_imports:
            for file_import in file_imports:
                modulename, function_names = file_import
                module = importlib.import_module(modulename)
                if function_names:
                    functions_ = [
                        f
                        for n, f in getmembers(module, isfunction)
                        if f.__module__ == modulename and n in function_names
                    ]
                else:
                    functions_ = [
                        f
                        for _, f in getmembers(module, isfunction)
                        if f.__module__ == modulename
                    ]
                for f_ in functions_:
                    function_id = f"{modulename}__{f_.__name__}"
                    self.functions[function_id] = f_
                    f_description = self.function_analyzer.analyze_function(f_)
                    f_description["function"]["name"] = function_id
                    self.function_descriptions[function_id] = f_description
                    self.function_origins[function_id] = {
                        "module_name": modulename,
                        "function_name": f_.__name__,
                    }

        # set up directory
        chroma_dir = chroma_base_dir + chroma_sub_dir
        Path(chroma_dir).mkdir(parents=True, exist_ok=True)

        # vector store
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = self.chroma_client.get_or_create_collection(name="tulip")
        embedded_functions = self.collection.get(include=["metadatas"])
        embedded_functions_ids = embedded_functions["ids"]

        # load functions as available in vector store
        _local_functions = {
            name: f for name, f in getmembers(sys.modules[__name__]) if isfunction(f)
        }
        for md in embedded_functions["metadatas"]:
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
                self.functions[identifier] = _local_functions["identifier"]

        if self.functions:
            new_functions = {
                n: d
                for n, d in self.functions.items()
                if n not in embedded_functions_ids
            }
            new_function_descriptions = {
                n: d
                for n, d in self.function_descriptions.items()
                if n not in embedded_functions_ids
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
                            "module": (
                                self.function_origins[f]["module_name"]
                                if f in self.function_origins
                                else ""
                            ),
                            "name": (
                                self.function_origins[f]["function_name"]
                                if f in self.function_origins
                                else ""
                            ),
                        }
                        for f in new_function_descriptions
                    ],
                    ids=[
                        val["function"]["name"]
                        for fd, val in new_function_descriptions.items()
                    ],
                )

    def add_function(
        self,
        function,
        modulename: str = None,
    ) -> None:
        function_id = (
            f"{modulename}__{function.__name__}" if modulename else function.__name__
        )
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
                    "module": modulename,
                    "name": function.__name__,
                }
            ],
            ids=[function_id],
        )
        self.function_origins[function_id] = {
            "module_name": modulename,
            "function_name": function.__name__,
        }
        logger.info(f"Added function {function_id} to collection {self.collection}.")

    def load_functions_from_file(
        self,
        modulename: str,
        function_names: list[str] = None,
    ) -> None:
        self.file_imports.append((modulename, function_names))
        module = importlib.import_module(modulename)
        if function_names:
            functions = [
                f
                for n, f in getmembers(module, isfunction)
                if f.__module__ == modulename and n in function_names
            ]
        else:
            functions = [
                f
                for _, f in getmembers(module, isfunction)
                if f.__module__ == modulename
            ]
        for f in functions:
            self.add_function(function=f, modulename=modulename)

    def remove_function(
        self,
        function_name: str,
    ) -> None:
        self.collection.delete(ids=[function_name])
        self.functions.pop(function_name)
        self.function_descriptions.pop(function_name)
        logger.info(
            f"Removed function {function_name} from collection {self.collection}."
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
        function_name: str,
        function_args: dict,
    ):
        try:
            res = self.functions[function_name](**function_args)
        except Exception as e:
            logger.error(e)
            res = f"Invalid tool call for {function_name}. Continue without this information."
        return res
