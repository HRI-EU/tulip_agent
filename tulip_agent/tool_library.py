#!/usr/bin/env python3
"""
The tool library (tulip) for the agent
"""
import importlib
import json
import logging
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
        classes: list = None,
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
        self.classes = classes if classes else []
        self.class_function_descriptions = (
            {c: [self.function_analyzer.analyze_class(c)] for c in self.classes}
            if classes
            else {}
        )

        # import tools from file
        self.file_imports = file_imports if file_imports else []
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
                    self.functions[f"{modulename}.{f_.__name__}"] = f_
                    f_description = self.function_analyzer.analyze_function(f_)
                    f_description["function"]["name"] = f"{modulename}.{f_.__name__}"
                    self.function_descriptions[f"{modulename}.{f_.__name__}"] = (
                        f_description
                    )

        # set up directory
        chroma_dir = chroma_base_dir + chroma_sub_dir
        Path(chroma_dir).mkdir(parents=True, exist_ok=True)

        # vector store
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = self.chroma_client.get_or_create_collection(name="tulip")
        if self.functions:
            embedded_functions = self.collection.get(include=[])["ids"]
            new_functions = {
                n: d for n, d in self.functions.items() if n not in embedded_functions
            }
            new_function_descriptions = {
                n: d
                for n, d in self.function_descriptions.items()
                if n not in embedded_functions
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
                        {"description": str(d)}
                        for d in new_function_descriptions.values()
                    ],
                    ids=[
                        val["function"]["name"]
                        for fd, val in new_function_descriptions.items()
                    ],
                )
        # TODO: handle classes

    def add_function(
        self,
        function,
        modulename: str = None,
    ) -> None:
        function_name = (
            f"{modulename}.{function.__name__}" if modulename else function.__name__
        )
        self.functions[function_name] = function
        function_data = self.function_analyzer.analyze_function(function)
        function_data["function"]["name"] = function_name
        self.function_descriptions[function_name] = function_data
        self.collection.add(
            documents=json.dumps(function_data, indent=4),
            embeddings=[embed(function_data["function"]["description"])],
            metadatas=[{"description": str(function_data)}],
            ids=[function_name],
        )
        logger.info(f"Added function {function_name} to collection {self.collection}.")

    def add_class(
        self,
        function_class,
    ) -> None:
        self.classes.append(function_class)
        self.class_function_descriptions[function_class] = [
            self.function_analyzer.analyze_class(function_class)
        ]
        # TODO: load into vector store

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

    def remove_class(
        self,
        class_name: str,
    ) -> None:
        # TODO
        pass

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
