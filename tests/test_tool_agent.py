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
from tests.example_tools import add, slow
from tulip_agent import CotToolAgent, NaiveToolAgent, Tool


def test_naive_tool_query(fake_chat_client):
    # FakeChatClient has an explicit branch for the simple `2+2` add-tool flow.
    agent = NaiveToolAgent(functions=[add], base_client=fake_chat_client)

    res = agent.query(prompt="What is 2+2?")

    _check_res(res, agent.messages)


def test_naive_tool_query_no_tools(fake_chat_client):
    agent = NaiveToolAgent(functions=[], base_client=fake_chat_client)

    res = agent.query(prompt="What is 2+2?")

    assert "4" in res
    assert len(agent.tools) == 1
    assert (
        _get_tool_by_name(agent.tools, "stop").definition["function"]["name"] == "stop"
    )


def test_cot_tool_query(fake_chat_client):
    agent = CotToolAgent(functions=[add], base_client=fake_chat_client)

    res = agent.query(prompt="What is 2+2?")

    _check_res(res, agent.messages)


def test_naive_tool_timeout(fake_chat_client):
    # The fake LLM only calls `slow` when the prompt mentions the slow-tool scenario.
    agent = NaiveToolAgent(functions=[slow], base_client=fake_chat_client)
    _get_tool_by_name(agent.tools, "slow").timeout = 0.05

    _ = agent.query(
        prompt=(
            "Try to run the slow function with a duration of 10. "
            "You may only run this once, then stop."
        )
    )

    slow_messages = [
        message
        for message in agent.messages
        if isinstance(message, dict) and message.get("name") == "slow"
    ]
    assert len(slow_messages) == 1
    assert (
        "Error: The tool did not return a response within the specified timeout."
        in slow_messages[0]["content"]
    )


def _check_res(res: str, messages: list):
    assert "4" in res
    assert "add" in _tool_message_names(messages)


def _tool_message_names(messages: list) -> list[str]:
    return [
        message["name"]
        for message in messages
        if isinstance(message, dict) and message.get("role") == "tool"
    ]


def _get_tool_by_name(tools: list[Tool], name: str) -> Tool:
    for tool in tools:
        if tool.unique_id == name:
            return tool
    raise ValueError(f"Tool {name} not found.")
