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
Analysis of Python functions and entire classes using introspection
for creating descriptions usable with the OpenAI API

Note: Only OPENAI_TYPES are supported as function inputs
"""
import inspect
import typing
from dataclasses import dataclass


OPENAI_BASE_TYPES = {
    float: "number",
    int: "number",
    str: "string",
    bool: "boolean",
}

OPENAI_NESTED_TYPES = {
    list: "array",
    tuple: "array",
    set: "array",
}


@dataclass
class VariableDescription:
    name: str
    type_: type
    description: str

    def __post_init__(self):
        # NOTE: assumes simple type hint structure; uses first type if there are distinct ones
        def _recurse(type_):
            if type_ in OPENAI_BASE_TYPES:
                return [OPENAI_BASE_TYPES[type_]]
            elif typing.get_origin(type_) in OPENAI_NESTED_TYPES:
                type_origin = OPENAI_NESTED_TYPES[typing.get_origin(type_)]
                type_args = _recurse(typing.get_args(type_)[0])
                return [type_origin] + type_args
            else:
                raise TypeError(
                    f"Unexpected subtype for {self.name}: {str(self.type_)}."
                )

        self.type_structure = _recurse(type_=self.type_)

    def to_dict(self) -> dict:
        base_result = {
            self.name: {
                "type": self.type_structure[0],
                "description": self.description,
            }
        }
        if len(self.type_structure) > 1:
            sub = base_result[self.name]
            for t in self.type_structure[1:]:
                sub["items"] = {"type": t}
                sub = sub["items"]
        return base_result


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
        signature = inspect.signature(function_)
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
            and signature.parameters.get(th).default is inspect.Parameter.empty
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
        descriptions = [e.strip() for e in function_.__doc__.split(":param ")]
        function_description, param_descriptions = descriptions[0], descriptions[1:]
        param_descriptions = {
            k: v
            for (k, v) in [
                e.split(":return:")[0].strip().split(": ")
                for e in param_descriptions
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
