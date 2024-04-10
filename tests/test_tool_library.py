#!/usr/bin/env python3
import unittest

from tulip_agent.tool_library import ToolLibrary


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


class TestCore(unittest.TestCase):
    def setUp(self):
        tulip = ToolLibrary(chroma_sub_dir="test/")
        tulip.chroma_client.delete_collection("tulip")

    def test_init(self):
        tulip = ToolLibrary(chroma_sub_dir="test/", functions=[add, subtract])
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {"add", "subtract"},
            "Initializing tool library with functions failed.",
        )

    def test_search_function(self):
        tulip = ToolLibrary(chroma_sub_dir="test/", functions=[add, subtract])
        res = tulip.search(problem_description="add 4 and 5", top_k=1)
        self.assertEqual(res["ids"][0][0], "add", "Searching for function failed.")

    def test_add_function(self):
        tulip = ToolLibrary(chroma_sub_dir="test/", functions=[subtract])
        tulip.add_function(function=add)
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(set(functions), {"add", "subtract"}, "Adding function failed.")

    def test_remove_function(self):
        tulip = ToolLibrary(chroma_sub_dir="test/", functions=[add, subtract])
        tulip.remove_function(function_name="add")
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(set(functions), {"subtract"}, "Removing function failed.")

    def test_load_all_from_file(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", [])]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {"example_tools.divide", "example_tools.multiply"},
            "Loading all functions from file failed.",
        )

    def test_load_names_from_file(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", ["multiply"])]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {"example_tools.multiply"},
            "Loading selected functions from file failed.",
        )

    def test_load_functions_from_file(self):
        tulip = ToolLibrary(chroma_sub_dir="test/")
        tulip.load_functions_from_file(
            modulename="example_tools", function_names=["multiply"]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {"example_tools.multiply"},
            "Loading selected functions from file failed.",
        )

    def test_execute(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", ["multiply"])]
        )
        res = tulip.execute(
            function_name="example_tools.multiply", function_args={"a": 2.0, "b": 2.0}
        )
        self.assertEqual(
            res,
            4.0,
            "Function execution via tool library failed.",
        )


if __name__ == "__main__":
    unittest.main()
