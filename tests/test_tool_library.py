#!/usr/bin/env python3
import shutil

from pathlib import Path

from tulip.tool_library import ToolLibrary


def add(a: float, b: float) -> float:
    """
    Add two numbers.

    :param a: The first number.
    :param b: The second number.
    :return: The sum of a and b.
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """
    Subtract two numbers.

    :param a: The number to be subtracted from.
    :param b: The number to subtract.
    :return: The difference of a and b.
    """
    return a - b


dir_path = Path("../data/chroma/test")
if dir_path.exists() and dir_path.is_dir():
    shutil.rmtree(dir_path)

tulip = ToolLibrary(chroma_sub_dir="test/", functions=[add, subtract])

res = tulip.search(problem_description="add 4 and 5", top_k=1)
assert res["ids"][0][0] == "add"

functions = tulip.collection.get(include=[])["ids"]
assert set(functions) == {"add", "subtract"}

tulip.remove_function(function_name="add")
functions = tulip.collection.get(include=[])["ids"]
assert set(functions) == {"subtract"}

tulip.add_function(function=add)
functions = tulip.collection.get(include=[])["ids"]
assert set(functions) == {"add", "subtract"}
