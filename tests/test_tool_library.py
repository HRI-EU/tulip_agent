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
import subprocess
import unittest

from tulip_agent.tool_library import ToolLibrary


class TestToolLibrary(unittest.TestCase):
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
                "example_tools__slow",
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
                "example_tools__slow",
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
                "example_tools__slow",
            },
            "Removing function failed.",
        )

    def test_execute(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", ["multiply"])]
        )
        res, error = tulip.execute(
            function_id="example_tools__multiply", function_args={"a": 2.0, "b": 2.0}
        )
        self.assertEqual(error, False, "Function execution failed.")
        self.assertEqual(
            res,
            4.0,
            "Function execution via tool library failed.",
        )

    def test_execute_timeout(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/",
            file_imports=[("example_tools", ["slow"])],
            default_timeout=1,
        )
        res, error = tulip.execute(
            function_id="example_tools__slow", function_args={"duration": 2}
        )
        self.assertEqual(error, True, "Function execution succeeded despite timeout.")
        self.assertEqual(
            res,
            "Error: The tool did not return a response within the specified timeout.",
            "Timeout did not return correct error message.",
        )

    def test_execute_unknown_tool(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", [])]
        )
        res, error = tulip.execute(
            function_id="example_tools__unknown", function_args={}
        )
        self.assertEqual(error, True, "Calling unknown function not caught.")
        self.assertEqual(
            res,
            "Error: example_tools__unknown is not a valid tool. Use only the tools available.",
            "Catching unknown function did not return correct error message.",
        )

    def test_execute_invalid_arguments(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_tools", ["multiply"])]
        )
        res, error = tulip.execute(
            function_id="example_tools__multiply", function_args={"a": 1, "wrong": 2}
        )
        self.assertEqual(
            error, True, "Function execution succeeded despite wrong arguments."
        )
        self.assertEqual(
            res,
            (
                "Error: Invalid tool call for example_tools__multiply: multiply() "
                "got an unexpected keyword argument 'wrong'"
            ),
            "Catching call with invalid arguments did not return correct error message.",
        )

    def test_update_function(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_module", [])]
        )
        function_id = "example_module__example"
        res, error = tulip.execute(
            function_id=function_id, function_args={"text": "unchanged"}
        )
        self.assertEqual(error, False, "Function execution failed.")
        self.assertEqual(res, "unchanged", "Initial function execution failed.")
        # overwrite function
        code = (
            "def example(text: str) -> str:\n"
            '    """\n'
            "    Returns the input.\n"
            "\n"
            "    :param text: Input text.\n"
            "    :return: The input text.\n"
            '    """\n'
            '    return "success"\n'
        )
        module_path = tulip.function_origins[function_id]["module_path"]
        with open(module_path, "w") as m:
            m.write(code)
        tulip.update_function(function_id=function_id)
        res, error = tulip.execute(
            function_id=function_id, function_args={"text": "failure"}
        )
        self.assertEqual(error, False, "Function execution failed.")
        self.assertEqual(
            res, "success", "Executing the function after updating the module failed."
        )
        example_module_path = tulip.function_origins[function_id]["module_path"]
        subprocess.run(["git", "checkout", "HEAD", "--", example_module_path])


if __name__ == "__main__":
    unittest.main()
