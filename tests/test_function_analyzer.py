#!/usr/bin/env python3
import json
from typing import Optional, Union

from tulip.function_analyzer import FunctionAnalyzer


def dummy_function(
    texts: list[str],
    number: Union[int, float],
    str_one: Optional[str],
    str_two: str = None,
) -> None:
    """
    Print some fine information.

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


fa = FunctionAnalyzer()
res = fa.analyze_function(dummy_function)
print(json.dumps(res, indent=4))

assert res["function"]["parameters"]["required"] == [
    "texts",
    "number",
], "Identifying optional parameters failed."
assert [k for k, _ in res["function"]["parameters"]["properties"].items()] == [
    "texts",
    "number",
    "str_one",
    "str_two",
], "Identifying parameters failed."
