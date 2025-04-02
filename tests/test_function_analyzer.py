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
import unittest
from typing import Optional, Union

from tulip_agent.function_analyzer import FunctionAnalyzer


def dummy_function(
    required: int,
    texts: list[str],
    number: Union[int, float],
    str_one: Optional[str] = None,
    str_two: str = "a",
    optional: int = 10,
) -> None:
    """
    Print some fine information.

    Some more information.

    :param required: Simple required parameter.
    :param texts: A list of strings.
    :param number: Some number.
    :param str_one: An optional string.
    :param str_two: Another optional string.
    :param optional: Optional parameter with default value.
    :return: Nothing.
    """
    print(required)
    print(texts)
    print(number)
    print(str_one)
    print(str_two)
    print(optional)
    return None


def nested_function(
    nested: list[list[list[set[str]]]],
) -> None:
    """
    Print some fine information.

    :param nested: A four-dimensional array of strings.
    :return: Nothing.
    """
    print(nested)
    return None


class Calculator:
    def __init__(self, divisor: float) -> None:
        self.divisor = divisor

    @staticmethod
    def add(a: float, b: float) -> float:
        """
        Add two numbers.

        :param a: The first number.
        :param b: The second number.
        :return: The sum of a and b.
        """
        return a + b

    @staticmethod
    def say_hi() -> None:
        """
        Print "hi".
        """
        print("hi")

    def custom_division(self, number: float) -> float:
        """
        Divides a number by the calculator's divisor attribute.

        :param number: The number to be subtracted from.
        :return: The result of number divided by the divisor attribute.
        """
        return number / self.divisor


class TestFunctionAnalyzer(unittest.TestCase):

    def setUp(self):
        self.fa = FunctionAnalyzer()

    def test_function_description(self):
        res = self.fa.analyze_function(dummy_function)
        self.assertEqual(
            res["function"]["description"],
            "Print some fine information.\n\n    Some more information.",
            "Identifying function description failed.",
        )

    def test_required_identification(self):
        res = self.fa.analyze_function(dummy_function)
        self.assertEqual(
            res["function"]["parameters"]["required"],
            [
                "required",
                "texts",
                "number",
            ],
            "Identifying optional parameters failed.",
        )

    def test_parameter_identification(self):
        res = self.fa.analyze_function(dummy_function)
        self.assertEqual(
            [k for k, _ in res["function"]["parameters"]["properties"].items()],
            [
                "required",
                "texts",
                "number",
                "str_one",
                "str_two",
                "optional",
            ],
            "Identifying parameters failed.",
        )

    def test_parameter_type_origin(self):
        res = self.fa.analyze_function(nested_function)
        self.assertEqual(
            res["function"]["parameters"]["properties"]["nested"]["type"],
            "array",
            "Resolving parameter type origin failed.",
        )

    def test_parameter_types_nested(self):
        res = self.fa.analyze_function(nested_function)
        self.assertEqual(
            res["function"]["parameters"]["properties"]["nested"]["items"],
            {
                "items": {
                    "items": {
                        "items": {"type": "string"},
                        "type": "array",
                        "uniqueItems": True,
                    },
                    "type": "array",
                },
                "type": "array",
            },
            "Resolving nested parameter types failed.",
        )

    def test_parameter_description(self):
        res = self.fa.analyze_function(nested_function)
        self.assertEqual(
            res["function"]["parameters"]["properties"]["nested"]["description"],
            "A four-dimensional array of strings.",
            "Resolving parameter description failed.",
        )

    def test_analyze_class(self):
        res = self.fa.analyze_class(Calculator)
        expected_descriptions = [
            {
                "type": "function",
                "function": {
                    "name": "add",
                    "description": "Add two numbers.",
                    "parameters": {
                        "additionalProperties": False,
                        "properties": {
                            "a": {
                                "title": "A",
                                "type": "number",
                                "description": "The first number.",
                            },
                            "b": {
                                "title": "B",
                                "type": "number",
                                "description": "The second number.",
                            },
                        },
                        "required": ["a", "b"],
                        "type": "object",
                    },
                },
                "strict": True,
            },
            {
                "type": "function",
                "function": {
                    "name": "custom_division",
                    "description": "Divides a number by the calculator's divisor attribute.",
                    "parameters": {
                        "additionalProperties": False,
                        "properties": {
                            "number": {
                                "title": "Number",
                                "type": "number",
                                "description": "The number to be subtracted from.",
                            }
                        },
                        "required": ["number"],
                        "type": "object",
                    },
                },
                "strict": True,
            },
            {
                "type": "function",
                "function": {
                    "name": "say_hi",
                    "description": 'Print "hi".',
                    "parameters": {
                        "additionalProperties": False,
                        "properties": {},
                        "type": "object",
                    },
                },
                "strict": True,
            },
        ]
        for expected_description in expected_descriptions:
            self.assertIn(
                expected_description,
                res,
                f"Analyzing class failed for {expected_description['function']['name']}.",
            )
        self.assertEqual(
            len(res),
            len(expected_descriptions),
            f"Analyzing class failed: len(res) instead of {len(expected_descriptions)} functions.",
        )


if __name__ == "__main__":
    unittest.main()
