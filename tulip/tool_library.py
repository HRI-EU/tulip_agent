#!/usr/bin/env python3
"""
The tool library (tulip) for the agent
"""
import json
import logging
import chromadb

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

        # set up directory
        chroma_dir = chroma_base_dir + chroma_sub_dir
        Path(chroma_dir).mkdir(parents=True, exist_ok=True)

        # vector store
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = self.chroma_client.get_or_create_collection(name="tulip")
        if functions:
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
    ) -> None:
        self.functions[function.__name__] = function
        function_data = self.function_analyzer.analyze_function(function)
        self.function_descriptions[function.__name__] = function_data
        self.collection.add(
            documents=json.dumps(function_data, indent=4),
            embeddings=[embed(function_data["function"]["description"])],
            metadatas=[{"description": str(function_data)}],
            ids=[function_data["function"]["name"]],
        )
        logger.info(
            f"Added function {function.__name__} to collection {self.collection}."
        )

    def add_class(
        self,
        function_class,
    ) -> None:
        self.classes.append(function_class)
        self.class_function_descriptions[function_class] = [
            self.function_analyzer.analyze_class(function_class)
        ]
        # TODO: load into vector store

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
        return self.functions[function_name](**function_args)
