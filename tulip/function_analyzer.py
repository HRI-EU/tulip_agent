#!/usr/bin/env python3
"""
Analysis of Python functions and entire classes using introspection
for creating descriptions usable with the OpenAI API
"""
import typing

from dataclasses import dataclass
from typing import Union


@dataclass
class VariableDescription:
    name: str
    type: str
    description: str

    def to_dict(self) -> dict:
        return {self.name: {"type": self.type, "description": self.description}}


class FunctionAnalyzer:
    openai_types = {
        float: "number",
        int: "number",
        str: "string",
    }

    def analyze_function(self, function_) -> dict:
        """
        Analyzes a python function and returns a description compatible with the OpenAI API
        Assumptions:
        * docstring includes a function description and parameter descriptions separated by 2 linebreaks
        * docstring includes parameter descriptions indicated by :param x:
        NOTE: for now, only simple file types are supported; they may be optional
        """
        name = function_.__name__

        # analyze type hints
        type_hints = typing.get_type_hints(function_)
        type_hints.pop("return", None)
        required = [
            th
            for th in type_hints
            if not (
                typing.get_origin(type_hints[th]) is Union
                and type(None) in typing.get_args(type_hints[th])
            )
        ]
        type_hints_basic = {
            k: (
                v
                if k in required
                else [t for t in typing.get_args(type_hints[k]) if t][0]
            )
            for k, v in type_hints.items()
        }

        # analyze doc string
        function_description, param_description = (
            e.strip() for e in function_.__doc__.split("\n\n")
        )
        param_descriptions = {
            k: v
            for (k, v) in [
                e.strip().split(": ") for e in param_description.split(":return:")[0].split(":param ") if e
            ]
        }
        variable_descriptions = [
            VariableDescription(
                name=v,
                type=self.openai_types[type_hints_basic[v]],
                description=param_descriptions[v],
            ).to_dict()
            for v in type_hints_basic
        ]
        properties = {k: v for d in variable_descriptions for k, v in d.items()}

        return {
            "name": name,
            "description": function_description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        }

    def analyze_class(self, class_: object) -> list:
        """
        Analyzes a python class and returns a description of all its non-private functions
            compatible with the OpenAI API
        """
        functions = [
            self.analyze_function(getattr(class_, func))
            for func in dir(class_)
            if callable(getattr(class_, func)) and not func.startswith("_")
        ]
        return functions
