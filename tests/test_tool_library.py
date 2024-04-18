#!/usr/bin/env python3
import unittest

from tulip_agent.tool_library import ToolLibrary


class TestCore(unittest.TestCase):
    def setUp(self):
        tulip = ToolLibrary(chroma_sub_dir="test/")
        tulip.chroma_client.delete_collection("tulip")

    def test_init(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", [])]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "example_tools__add",
                "example_tools__subtract",
                "example_tools__multiply",
                "example_tools__divide",
            },
            "Initializing tool library with functions failed.",
        )

    def test_init_specific(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", ["add"])]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {"example_tools__add"},
            "Initializing tool library with selected functions failed.",
        )

    def test_load_file(self):
        tulip = ToolLibrary(chroma_sub_dir="test/")
        tulip.load_functions_from_file(module_name="example_tools", function_names=[])
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "example_tools__add",
                "example_tools__subtract",
                "example_tools__multiply",
                "example_tools__divide",
            },
            "Loading entire file failed.",
        )

    def test_load_names_from_file(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", ["multiply"])]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {"example_tools__multiply"},
            "Loading selected functions from file failed.",
        )

    def test_search_function(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", [])]
        )
        res = tulip.search(problem_description="add 4 and 5", top_k=1)
        self.assertEqual(
            res["ids"][0][0], "example_tools__add", "Searching for function failed."
        )

    def test_remove_function(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", [])]
        )
        tulip.remove_function(function_id="example_tools__add")
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "example_tools__subtract",
                "example_tools__multiply",
                "example_tools__divide",
            },
            "Removing function failed.",
        )

    def test_execute(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", ["multiply"])]
        )
        res = tulip.execute(
            function_id="example_tools__multiply", function_args={"a": 2.0, "b": 2.0}
        )
        self.assertEqual(
            res,
            4.0,
            "Function execution via tool library failed.",
        )


if __name__ == "__main__":
    unittest.main()
