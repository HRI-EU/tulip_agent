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
import pytest

from tests import example_tools
from tests.example_tools_in_class import Calculator
from tulip_agent import (
    AutoTulipAgent,
    CotTulipAgent,
    DfsTulipAgent,
    FunctionAnalyzer,
    ImportedTool,
    InformedCotTulipAgent,
    MinimalTulipAgent,
    NaiveTulipAgent,
    OneShotCotTulipAgent,
    PrimedCotTulipAgent,
)


@pytest.mark.parametrize(
    "agent_class",
    [
        NaiveTulipAgent,
        MinimalTulipAgent,
        CotTulipAgent,
        InformedCotTulipAgent,
        OneShotCotTulipAgent,
        PrimedCotTulipAgent,
        AutoTulipAgent,
    ],
)
def test_tulip_agent_query(agent_class, tulip, fake_chat_client):
    # FakeChatClient is intentionally scripted for this simple math/retrieval flow.
    agent = agent_class(tool_library=tulip, base_client=fake_chat_client)

    res = agent.query(prompt="What is 2+2?")

    assert "4" in res
    assert "add" in _tool_message_names(agent.messages)


def test_dfs_tulip_query(tulip, fake_chat_client):
    # DFS gets a fake empty decomposition for `2+2`, then executes the add tool.
    agent = DfsTulipAgent(tool_library=tulip, base_client=fake_chat_client)

    res = agent.query(prompt="What is 2+2?")

    assert "4" in res
    assert "add" in [tc.unique_id for tc in agent.task.tool_candidates]


def test_cot_tulip_query_with_instance(tool_library_factory, fake_chat_client):
    calculator = Calculator(divisor=3)
    tulip = tool_library_factory(
        instance_imports=[calculator],
        description="Various math tools.",
    )
    agent = CotTulipAgent(tool_library=tulip, base_client=fake_chat_client)

    res = agent.query(prompt="What is 2+2?")

    assert "4" in res
    assert "add" in _tool_message_names(agent.messages)


def test_default_tools(tulip, fake_chat_client):
    character = (
        "You must solve the task provided by the user using a tool. "
        "Eventually use the speak function to tell them the result."
    )
    agent = MinimalTulipAgent(
        tool_library=tulip,
        default_tools=[tulip.tools["speak"]],
        top_k_functions=1,
        instructions=character,
        base_client=fake_chat_client,
    )

    res = agent.query(prompt="What is 2+2?")

    tool_message_names = _tool_message_names(agent.messages)
    assert "4" in res
    assert "speak" in tool_message_names


def test_default_tools_must_exist_in_library(tulip, fake_chat_client):
    missing_tool = ImportedTool.from_function(
        function=example_tools.add,
        definition=FunctionAnalyzer.analyze_function(example_tools.add),
        verbose_id=True,
    )

    with pytest.raises(ValueError, match="not available in tool library"):
        MinimalTulipAgent(
            tool_library=tulip,
            default_tools=[missing_tool],
            base_client=fake_chat_client,
        )


@pytest.fixture
def tulip(tool_library_factory):
    return tool_library_factory(
        file_imports=[("tests.example_tools", [])],
        description="Various math tools.",
    )


def _tool_message_names(messages: list) -> list[str]:
    return [
        message["name"]
        for message in messages
        if isinstance(message, dict) and message.get("role") == "tool"
    ]
