#!/usr/bin/env python3
"""
Analysis of Python functions and entire classes using introspection
for creating descriptions usable with the OpenAI API

Note: Only OPENAI_TYPES are supported as function inputs
"""
import typing

from dataclasses import dataclass


OPENAI_BASE_TYPES = {
    float: "number",
    int: "number",
    str: "string",
}

OPENAI_NESTED_TYPES = {
    list: "array",
}


@dataclass
class VariableDescription:
    name: str
    type_: type
    description: str

    def __post_init__(self):
        if self.type_ in OPENAI_BASE_TYPES:
            self.type_origin = OPENAI_BASE_TYPES[self.type_]
            self.type_arg = None
        elif typing.get_origin(self.type_) in OPENAI_NESTED_TYPES:
            self.type_origin = OPENAI_NESTED_TYPES[typing.get_origin(self.type_)]
            self.type_arg = OPENAI_BASE_TYPES[typing.get_args(self.type_)[0]]
        else:
            raise TypeError(f"Unexpected subtype for {self.name}: {str(self.type_)}.")

    def to_dict(self) -> dict:
        if self.type_arg is None:
            return {
                self.name: {
                    "type": self.type_origin,
                    "description": self.description,
                }
            }
        else:
            return {
                self.name: {
                    "type": self.type_origin,
                    "description": self.description,
                    "items": {"type": self.type_arg},
                }
            }


class FunctionAnalyzer:

    @staticmethod
    def analyze_function(function_) -> dict:
        """
        Analyzes a python function and returns a description compatible with the OpenAI API
        Assumptions:
        * docstring includes a function description and parameter descriptions separated by 2 linebreaks
        * docstring includes parameter descriptions indicated by :param x:
        NOTE:
        * for now, only simple file types and lists thereof are supported
        * inputs may be optional
        * inputs that are unions default to the first type; [int, str] -> int (which is interpreted as number)
        """
        name = function_.__name__

        # analyze type hints
        type_hints = typing.get_type_hints(function_)
        type_hints.pop("return", None)
        required = [
            th
            for th in type_hints
            if not (
                typing.get_origin(type_hints[th]) is typing.Optional
                or typing.get_origin(type_hints[th]) is typing.Union
                and type(None) in typing.get_args(type_hints[th])
            )
        ]
        type_hints_basic = {
            k: (
                v
                if typing.get_origin(v) is not typing.Union
                else (
                    typing.get_args(v)[0]
                    if k in required
                    else [t for t in typing.get_args(type_hints[k]) if t][0]
                )
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
                e.strip().split(": ")
                for e in param_description.split(":return:")[0].split(":param ")
                if e
            ]
        }
        variable_descriptions = [
            VariableDescription(
                name=v,
                type_=type_hints_basic[v],
                description=param_descriptions[v],
            ).to_dict()
            for v in type_hints_basic
        ]
        properties = {k: v for d in variable_descriptions for k, v in d.items()}

        return {
            "type": "function",
            "function": {
                "name": name,
                "description": function_description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
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
