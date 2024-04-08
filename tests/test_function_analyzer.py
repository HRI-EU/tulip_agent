#!/usr/bin/env python3
import unittest

from typing import Optional, Union

from tulip_agent.function_analyzer import FunctionAnalyzer


def dummy_function(
    texts: list[str],
    number: Union[int, float],
    str_one: Optional[str],
    str_two: str = None,
) -> None:
    """
    Print some fine information.

    Some more information.

    :param texts: A list of strings.
    :param number: Some number.
    :param str_one: An optional string.
    :param str_two: Another optional string.
    :return: Nothing.
    """
    print(texts)
    print(number)
    print(str_one)
    print(str_two)
    return None


class TestCore(unittest.TestCase):

    def setUp(self):
        self.fa = FunctionAnalyzer()
        self.res = self.fa.analyze_function(dummy_function)

    def test_required_identification(self):
        self.assertEqual(
            self.res["function"]["parameters"]["required"],
            [
                "texts",
                "number",
            ],
            "Identifying optional parameters failed.",
        )

    def test_parameter_identification(self):
        self.assertEqual(
            [k for k, _ in self.res["function"]["parameters"]["properties"].items()],
            [
                "texts",
                "number",
                "str_one",
                "str_two",
            ],
            "Identifying parameters failed.",
        )


if __name__ == "__main__":
    unittest.main()
