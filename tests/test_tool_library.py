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
