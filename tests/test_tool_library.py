#!/usr/bin/env python3
#
#  Copyright (c) 2024-2025, Honda Research Institute Europe GmbH
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  SPDX-License-Identifier: BSD-3-Clause
#
#
import subprocess
import unittest

from tests.example_tools_in_class import Calculator
from tulip_agent.tool_execution import Job, execute_parallel_jobs
from tulip_agent.tool_library import ToolLibrary


class TestToolLibrary(unittest.TestCase):
    def setUp(self):
        tulip = ToolLibrary(chroma_sub_dir="test/")
        tulip.chroma_client.delete_collection("tulip")

    def test_init(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("tests.example_tools", [])]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "add",
                "subtract",
                "multiply",
                "divide",
                "slow",
                "speak",
            },
            "Initializing tool library with functions failed.",
        )

    def test_init_verbose_id(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/",
            file_imports=[("tests.example_tools", [])],
            verbose_tool_ids=True,
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "tests__example_tools__add",
                "tests__example_tools__subtract",
                "tests__example_tools__multiply",
                "tests__example_tools__divide",
                "tests__example_tools__slow",
                "tests__example_tools__speak",
            },
            "Initializing tool library with functions failed.",
        )

    def test_init_specific(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("tests.example_tools", ["add"])]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {"add"},
            "Initializing tool library with selected functions failed.",
        )

    def test_init_instance(self):
        calculator = Calculator(divisor=3)
        tulip = ToolLibrary(chroma_sub_dir="test/", instance_imports=[calculator])
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "add",
                "custom_division",
            },
            "Initializing tool library with class instance failed.",
        )

    def test_init_instance_verbose_id(self):
        calculator = Calculator(divisor=3)
        tulip = ToolLibrary(
            chroma_sub_dir="test/",
            instance_imports=[calculator],
            verbose_tool_ids=True,
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "tests__example_tools_in_class__Calculator__add",
                "tests__example_tools_in_class__Calculator__custom_division",
            },
            "Initializing tool library with class instance failed.",
        )

    def test_init_file_unspecified(self):
        """
        The vector store should only contain the specified tools.
        If an existing store is loaded, all tools that are not specified should be removed.
        Here, a file is not specified in the second init.
        """
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("tests.example_tools", [])]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            len(functions),
            6,
            "Functions from file were not added in first initialization.",
        )
        tulip = ToolLibrary(chroma_sub_dir="test/")
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            len(functions),
            0,
            "Legacy functions from file were not removed in second initialization.",
        )

    def test_init_specific_unspecified(self):
        """
        The vector store should only contain the specified tools.
        If an existing store is loaded, all tools that are not specified should be removed.
        Here, a single function from a file is not specified in the second init.
        """
        tulip = ToolLibrary(
            chroma_sub_dir="test/",
            file_imports=[("tests.example_tools", ["add", "subtract"])],
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "add",
                "subtract",
            },
            "Specific functions from file were not added in first initialization.",
        )
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("tests.example_tools", ["add"])]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {"add"},
            "Unspecified legacy function from file were not removed in second initialization.",
        )

    def test_init_instance_unspecified(self):
        """
        The vector store should only contain the specified tools.
        If an existing store is loaded, all tools that are not specified should be removed.
        Here, an instance is not specified in the second init.
        """
        calculator = Calculator(divisor=3)
        tulip = ToolLibrary(chroma_sub_dir="test/", instance_imports=[calculator])
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            len(functions),
            2,
            "Instance functions were not added in first initialization.",
        )
        tulip = ToolLibrary(chroma_sub_dir="test/")
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            len(functions),
            0,
            "Legacy instance functions were not removed in second initialization.",
        )

    def test_init_name_clash(self):
        calculator = Calculator(divisor=3)
        with self.assertRaises(ValueError):
            _ = ToolLibrary(
                chroma_sub_dir="test/",
                file_imports=[("tests.example_tools", ["add"])],
                instance_imports=[calculator],
            )

    def test_init_no_name_clash(self):
        calculator = Calculator(divisor=3)
        tulip = ToolLibrary(
            chroma_sub_dir="test/",
            file_imports=[("tests.example_tools", ["add"])],
            instance_imports=[calculator],
            verbose_tool_ids=True,
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "tests__example_tools__add",
                "tests__example_tools_in_class__Calculator__add",
                "tests__example_tools_in_class__Calculator__custom_division",
            },
            "Initializing tool library with class instance failed.",
        )

    def test_load_file(self):
        tulip = ToolLibrary(chroma_sub_dir="test/")
        tulip.load_functions_from_file(
            module_name="tests.example_tools", function_names=[]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "add",
                "subtract",
                "multiply",
                "divide",
                "slow",
                "speak",
            },
            "Loading entire file failed.",
        )

    def test_load_instance(self):
        calculator = Calculator(divisor=3)
        tulip = ToolLibrary(chroma_sub_dir="test/")
        tulip.load_functions_from_instance(instance=calculator)
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "add",
                "custom_division",
            },
            "Loading entire file failed.",
        )

    def test_load_name_clash(self):
        calculator = Calculator(divisor=3)
        tulip = ToolLibrary(
            chroma_sub_dir="test/",
            file_imports=[("tests.example_tools", ["add"])],
        )
        with self.assertRaises(ValueError):
            tulip.load_functions_from_instance(instance=calculator)

    def test_load_names_from_file(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("tests.example_tools", ["multiply"])]
        )
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {"multiply"},
            "Loading selected functions from file failed.",
        )

    def test_search_function(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("tests.example_tools", [])]
        )
        res = tulip.search(problem_description="add 4 and 5", top_k=1)
        self.assertEqual(
            res[0].unique_id,
            "add",
            "Searching for function failed.",
        )

    def test_remove_tool(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("tests.example_tools", [])]
        )
        tulip.remove_tool(tool_id="add")
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            set(functions),
            {
                "subtract",
                "multiply",
                "divide",
                "slow",
                "speak",
            },
            "Removing function failed.",
        )

    def test_remove_tools_by_instance(self):
        calculator = Calculator(divisor=3)
        tulip = ToolLibrary(chroma_sub_dir="test/", instance_imports=[calculator])
        tulip.remove_tools_by_instance(instance=calculator)
        functions = tulip.collection.get(include=[])["ids"]
        self.assertEqual(
            len(functions),
            0,
            "Removing functions by instance failed.",
        )

    def test_update_tool(self):
        tulip = ToolLibrary(
            chroma_sub_dir="test/", file_imports=[("example_module", [])]
        )
        function_id = "example"
        initial_res = execute_parallel_jobs(
            jobs=[
                Job(
                    tool_call_id=function_id,
                    tool=tulip.tools[function_id],
                    parameters={"text": "unchanged"},
                )
            ]
        )
        self.assertIsNone(initial_res[0].result.error, "Function execution failed.")
        self.assertEqual(
            initial_res[0].result.value,
            "unchanged",
            "Initial function execution failed.",
        )
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
        with open(tulip.tools[function_id].module_path, "w") as m:
            m.write(code)
        tulip.update_tool(tool_id=function_id)
        updated_res = execute_parallel_jobs(
            jobs=[
                Job(
                    tool_call_id=function_id,
                    tool=tulip.tools[function_id],
                    parameters={"text": "failure"},
                )
            ]
        )
        self.assertIsNone(updated_res[0].result.error, "Function execution failed.")
        self.assertEqual(
            updated_res[0].result.value,
            "success",
            "Executing the function after updating the module failed.",
        )
        example_module_path = tulip.tools[function_id].module_path
        subprocess.run(["git", "checkout", "HEAD", "--", example_module_path])


if __name__ == "__main__":
    unittest.main()
