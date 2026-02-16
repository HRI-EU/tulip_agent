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
import unittest

from tests import example_tools
from tulip_agent.function_analyzer import FunctionAnalyzer
from tulip_agent.tool import ImportedTool
from tulip_agent.tool_execution import Job, execute_parallel_jobs


class TestToolExecution(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        function_analyzer = FunctionAnalyzer()
        cls.module_name = example_tools.__name__

        cls.multiply_tool = ImportedTool(
            module_name=cls.module_name,
            function_name=example_tools.multiply.__name__,
            definition=function_analyzer.analyze_function(example_tools.multiply),
        )
        cls.slow_tool = ImportedTool(
            module_name=cls.module_name,
            function_name=example_tools.slow.__name__,
            definition=function_analyzer.analyze_function(example_tools.slow),
            timeout=0.05,
            timeout_message="The tool did not return a response within the specified timeout.",
        )

    def test_execute(self):
        res = execute_parallel_jobs(
            jobs=[
                Job(
                    tool_call_id="test",
                    tool=self.multiply_tool,
                    parameters={"a": 2.0, "b": 2.0},
                ),
            ]
        )
        self.assertEqual(len(res), 1, "Did not return exactly one result for one job.")
        self.assertEqual(res[0].result.error, None, "Function execution failed.")
        self.assertEqual(
            res[0].result.value,
            4.0,
            "Function execution via tool library failed.",
        )

    def test_execute_timeout(self):
        res = execute_parallel_jobs(
            jobs=[
                Job(
                    tool_call_id="slow",
                    tool=self.slow_tool,
                    parameters={"duration": 1},
                ),
            ]
        )
        self.assertEqual(len(res), 1, "Did not return exactly one result for one job.")
        self.assertIsNone(res[0].result.value, "Timeout should not return a value.")
        self.assertIsNotNone(res[0].result.error, "Timeout should return an error.")
        self.assertIn(
            "Error: The tool did not return a response within the specified timeout.",
            res[0].result.error,
            "Timeout did not return correct error message.",
        )

    def test_execute_invalid_arguments(self):
        res = execute_parallel_jobs(
            jobs=[
                Job(
                    tool_call_id="invalid",
                    tool=self.multiply_tool,
                    parameters={"a": 1, "wrong": 2},
                ),
            ]
        )
        self.assertEqual(len(res), 1, "Did not return exactly one result for one job.")
        self.assertIsNone(
            res[0].result.value, "Invalid arguments should not return a value."
        )
        self.assertIn(
            "Error: Invalid tool call -",
            res[0].result.error,
            "Catching call with invalid arguments did not return correct error prefix.",
        )
        self.assertIn(
            "unexpected keyword argument 'wrong'",
            res[0].result.error,
            "Invalid argument details were not preserved.",
        )

    def test_execute_parallel_jobs_preserves_order(self):
        res = execute_parallel_jobs(
            jobs=[
                Job(
                    tool_call_id="first",
                    tool=self.multiply_tool,
                    parameters={"a": 1.0, "b": 1.0},
                ),
                Job(
                    tool_call_id="second",
                    tool=self.multiply_tool,
                    parameters={"a": 2.0, "b": 2.0},
                ),
                Job(
                    tool_call_id="third",
                    tool=self.multiply_tool,
                    parameters={"a": 3.0, "b": 3.0},
                ),
            ]
        )
        self.assertEqual(len(res), 3, "Did not return exactly three results.")
        self.assertEqual(
            [job.tool_call_id for job in res],
            ["first", "second", "third"],
            "Incorrect order.",
        )
        self.assertEqual(
            [job.result.value for job in res], [1.0, 4.0, 9.0], "Incorrect results."
        )
        self.assertTrue(
            all(job.result.error is None for job in res), "Unexpected error."
        )

    def test_execute_parallel_jobs_timeout(self):
        res = execute_parallel_jobs(
            jobs=[
                Job(
                    tool_call_id="slow",
                    tool=self.slow_tool,
                    parameters={"duration": 1},
                ),
                Job(
                    tool_call_id="fast",
                    tool=self.multiply_tool,
                    parameters={"a": 2.0, "b": 2.0},
                ),
            ]
        )
        self.assertEqual(len(res), 2, "Did not return exactly two results.")
        self.assertIsNotNone(
            res[0].result.error, "Expected timeout error for slow job."
        )
        self.assertIn(
            "The tool did not return a response within the specified timeout.",
            res[0].result.error,
        )
        self.assertEqual(res[1].result.value, 4.0)
        self.assertIsNone(res[1].result.error)


if __name__ == "__main__":
    unittest.main()
