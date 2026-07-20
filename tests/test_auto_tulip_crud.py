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
from tests.conftest import FakeChatResponse, FakeChoice, FakeMessage, FakeUsage
from tests.example_tools import add
from tulip_agent import AutoTulipAgent, NaiveToolAgent
from tulip_agent.tool_execution import Job, execute_parallel_jobs


def test_auto_tulip_create_update_delete_tool(
    tool_library_factory,
    fake_chat_client,
    monkeypatch,
    tmp_path,
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    tulip = tool_library_factory()
    agent = AutoTulipAgent(tool_library=tulip, base_client=fake_chat_client)
    generated_code = iter(
        [
            _scale_number_code("return number * 2"),
            _scale_number_code("return number * 3"),
        ]
    )
    monkeypatch.setattr(
        agent,
        "_generate_code",
        lambda task_description: next(generated_code),
    )

    create_result = agent.create_tool("scale a number")

    assert create_result == "Made tool `scale_number` available via the tool library."
    assert _execute_tool(tulip.tools["scale_number"], {"number": 5}) == 10

    update_result = agent.update_tool("scale_number", "Triple the number instead.")

    assert update_result == "Successfully updated `scale_number`."
    assert _execute_tool(tulip.tools["scale_number"], {"number": 5}) == 15

    delete_result = agent.delete_tool("scale_number")

    assert delete_result == "Removed tool scale_number from the tool library."
    assert "scale_number" not in tulip.tools


def test_tool_loop_returns_error_when_model_does_not_call_tool():
    agent = NaiveToolAgent(functions=[add], base_client=NoToolCallClient())

    res = agent.query(prompt="What is 2+2?")

    assert res == "Invalid response - no tool calls."


def _execute_tool(tool, parameters: dict) -> float:
    result = execute_parallel_jobs(
        jobs=[
            Job(
                tool_call_id=tool.unique_id,
                tool=tool,
                parameters=parameters,
            )
        ]
    )[0].result
    assert result.error is None
    return result.value


def _scale_number_code(return_statement: str) -> str:
    return (
        "def scale_number(number: float) -> float:\n"
        '    """\n'
        "    Scale a number.\n"
        "\n"
        "    :param number: The number to scale.\n"
        "    :return: The scaled number.\n"
        '    """\n'
        f"    {return_statement}\n"
    )


class NoToolCallClient:
    def __init__(self) -> None:
        self.chat = NoToolCallChat()


class NoToolCallChat:
    def __init__(self) -> None:
        self.completions = NoToolCallCompletions()


class NoToolCallCompletions:
    def create(self, **params) -> FakeChatResponse:
        return FakeChatResponse(
            choices=[FakeChoice(message=FakeMessage(content="not a tool call"))],
            id="fake-no-tool-call",
            usage=FakeUsage(),
        )
