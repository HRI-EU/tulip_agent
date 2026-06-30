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
import json

from tests import example_tools
from tests.conftest import FakeFunctionCall, FakeToolCall
from tulip_agent.function_analyzer import FunctionAnalyzer
from tulip_agent.tool import ImportedTool
from tulip_agent.tool_execution import Job, execute_parallel_jobs, execute_tool_calls


def test_execute():
    res = execute_parallel_jobs(
        jobs=[
            Job(
                tool_call_id="test",
                tool=_multiply_tool(),
                parameters={"a": 2.0, "b": 2.0},
            ),
        ]
    )
    assert len(res) == 1
    assert res[0].result.error is None
    assert res[0].result.value == 4.0


def test_execute_from_callable():
    res = execute_parallel_jobs(
        jobs=[
            Job(
                tool_call_id="test_callable",
                tool=_add_tool(),
                parameters={"a": 2.0, "b": 3.0},
            ),
        ]
    )
    assert len(res) == 1
    assert res[0].result.error is None
    assert res[0].result.value == 5.0


def test_execute_timeout():
    res = execute_parallel_jobs(
        jobs=[
            Job(
                tool_call_id="slow",
                tool=_slow_tool(),
                parameters={"duration": 1},
            ),
        ]
    )
    assert len(res) == 1
    assert res[0].result.value is None
    assert res[0].result.error is not None
    assert (
        "Error: The tool did not return a response within the specified timeout."
        in res[0].result.error
    )


def test_execute_invalid_arguments():
    res = execute_parallel_jobs(
        jobs=[
            Job(
                tool_call_id="invalid",
                tool=_multiply_tool(),
                parameters={"a": 1, "wrong": 2},
            ),
        ]
    )
    assert len(res) == 1
    assert res[0].result.value is None
    assert "Error: Invalid tool call -" in res[0].result.error
    assert "unexpected keyword argument 'wrong'" in res[0].result.error


def test_execute_parallel_jobs_preserves_order():
    res = execute_parallel_jobs(
        jobs=[
            Job(
                tool_call_id="first",
                tool=_multiply_tool(),
                parameters={"a": 1.0, "b": 1.0},
            ),
            Job(
                tool_call_id="second",
                tool=_multiply_tool(),
                parameters={"a": 2.0, "b": 2.0},
            ),
            Job(
                tool_call_id="third",
                tool=_multiply_tool(),
                parameters={"a": 3.0, "b": 3.0},
            ),
        ]
    )
    assert len(res) == 3
    assert [job.tool_call_id for job in res] == ["first", "second", "third"]
    assert [job.result.value for job in res] == [1.0, 4.0, 9.0]
    assert all(job.result.error is None for job in res)


def test_execute_parallel_jobs_timeout():
    res = execute_parallel_jobs(
        jobs=[
            Job(
                tool_call_id="slow",
                tool=_slow_tool(),
                parameters={"duration": 1},
            ),
            Job(
                tool_call_id="fast",
                tool=_multiply_tool(),
                parameters={"a": 2.0, "b": 2.0},
            ),
        ]
    )
    assert len(res) == 2
    assert res[0].result.error is not None
    assert "The tool did not return a response within the specified timeout." in (
        res[0].result.error
    )
    assert res[1].result.value == 4.0
    assert res[1].result.error is None


def test_execute_tool_calls_handles_invalid_json():
    messages = []
    tool_call = FakeToolCall(
        id="invalid-json",
        function=FakeFunctionCall(name="add", arguments="{"),
    )

    execute_tool_calls(tool_calls=[tool_call], messages=messages, tools={})

    assert messages == [
        {
            "tool_call_id": "invalid-json",
            "role": "tool",
            "name": "invalid_tool_call",
            "content": "Error: Invalid arguments for invalid_tool_call "
            "(previously add): Expecting property name enclosed in double quotes: "
            "line 1 column 2 (char 1)",
        }
    ]


def test_execute_tool_calls_rejects_unknown_tool():
    messages = []
    tool_call = FakeToolCall(
        id="unknown-tool",
        function=FakeFunctionCall(
            name="missing_tool",
            arguments=json.dumps({"a": 1}),
        ),
    )

    execute_tool_calls(tool_calls=[tool_call], messages=messages, tools={})

    assert messages == [
        {
            "tool_call_id": "unknown-tool",
            "role": "tool",
            "name": "invalid_tool_call",
            "content": "Error: missing_tool is not a valid tool. "
            "Use only the tools available.",
        }
    ]


def _multiply_tool():
    function_analyzer = FunctionAnalyzer()
    return ImportedTool.from_module(
        module_name=example_tools.__name__,
        function_name=example_tools.multiply.__name__,
        definition=function_analyzer.analyze_function(example_tools.multiply),
    )


def _slow_tool():
    function_analyzer = FunctionAnalyzer()
    return ImportedTool.from_module(
        module_name=example_tools.__name__,
        function_name=example_tools.slow.__name__,
        definition=function_analyzer.analyze_function(example_tools.slow),
        timeout=0.05,
        timeout_message="The tool did not return a response within the specified timeout.",
    )


def _add_tool():
    function_analyzer = FunctionAnalyzer()
    return ImportedTool.from_function(
        function=example_tools.add,
        definition=function_analyzer.analyze_function(example_tools.add),
    )
