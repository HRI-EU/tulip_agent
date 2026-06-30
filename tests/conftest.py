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
from dataclasses import dataclass
from typing import Any, Callable

import pytest

from tulip_agent import ToolLibrary


@dataclass
class FakeUsage:
    prompt_tokens: int = 1
    completion_tokens: int = 1


@dataclass
class FakeEmbeddingData:
    embedding: list[float]


@dataclass
class FakeEmbeddingResponse:
    data: list[FakeEmbeddingData]
    usage: FakeUsage


class FakeEmbeddings:
    def __init__(self) -> None:
        self.inputs: list[str] = []

    def create(
        self,
        model: str,
        input: str,
        encoding_format: str,
    ) -> FakeEmbeddingResponse:
        self.inputs.append(input)
        return FakeEmbeddingResponse(
            data=[FakeEmbeddingData(embedding=_semantic_embedding(input))],
            usage=FakeUsage(prompt_tokens=max(1, len(input.split()))),
        )


class FakeEmbeddingClient:
    def __init__(self) -> None:
        self.embeddings = FakeEmbeddings()


@dataclass
class FakeFunctionCall:
    name: str
    arguments: str


@dataclass
class FakeToolCall:
    id: str
    function: FakeFunctionCall


@dataclass
class FakeMessage:
    content: str | None = None
    role: str = "assistant"
    tool_calls: list[FakeToolCall] | None = None


@dataclass
class FakeChoice:
    message: FakeMessage
    finish_reason: str = "stop"
    index: int = 0


@dataclass
class FakeChatResponse:
    choices: list[FakeChoice]
    id: str
    usage: FakeUsage


class FakeCompletions:
    def __init__(self, client: "FakeChatClient") -> None:
        self.client = client

    def create(self, **params: Any) -> FakeChatResponse:
        self.client.calls.append(params)
        return self.client.response_for(params)


class FakeChat:
    def __init__(self, client: "FakeChatClient") -> None:
        self.completions = FakeCompletions(client)


class FakeChatClient:
    """Small deterministic chat-completions fake for the agent tests.

    This fake is scenario-based, not a general LLM simulator. Branches below
    intentionally document which prompt/tool flow they support and raise explicit
    errors when a prompt change makes a test request unrecognized.
    """

    def __init__(self) -> None:
        self.chat = FakeChat(self)
        self.calls: list[dict[str, Any]] = []
        self._tool_call_counter = 0

    def response_for(self, params: dict[str, Any]) -> FakeChatResponse:
        messages = params["messages"]
        tools = params.get("tools") or []
        tool_names = _tool_names(tools)
        last_prompt = _last_message_content(messages)
        all_message_content = _all_message_content(messages)

        if _expects_json(params, last_prompt):
            return self._json_response_for_prompt(last_prompt)

        if not tools:
            if _is_simple_math_prompt(all_message_content):
                return self._text_response("The result is 4.")
            raise _unexpected_fake_chat_request(
                "Text-only fake responses only support the simple `What is 2+2?` "
                "scenario.",
                params,
            )

        if "search_tools" in tool_names and "add" not in tool_names:
            if _is_tool_search_prompt(last_prompt) or _is_simple_math_prompt(
                all_message_content
            ):
                return self._tool_response(
                    "search_tools",
                    {"action_descriptions": ["add two numbers"]},
                )
            raise _unexpected_fake_chat_request(
                "Expected a prompt that asks the fake agent to search for tools. "
                "If the tool-search prompt changed intentionally, update this "
                "FakeChatClient branch.",
                params,
            )

        if (
            "slow" in tool_names
            and "slow" in all_message_content.lower()
            and not _tool_was_called(messages, "slow")
        ):
            return self._tool_response("slow", {"duration": 10})

        if "add" in tool_names and not _tool_was_called(messages, "add"):
            if _is_simple_math_prompt(
                all_message_content
            ) or _is_solve_with_tools_prompt(all_message_content):
                return self._tool_response("add", {"a": 2.0, "b": 2.0})
            raise _unexpected_fake_chat_request(
                "The fake add-tool branch only supports the simple math flow. "
                "If the test now covers different operands or prompt wording, "
                "teach the fake that scenario explicitly.",
                params,
            )

        if (
            "speak" in tool_names
            and (
                "speak" in all_message_content.lower()
                or "said" in all_message_content.lower()
            )
            and not _tool_was_called(messages, "speak")
        ):
            return self._tool_response("speak", {"text": "The result is 4."})

        if "stop" in tool_names:
            return self._tool_response("stop", {"message": "The result is 4."})

        raise _unexpected_fake_chat_request(
            "No fake chat branch matched this tool-enabled request.",
            params,
        )

    def _json_response_for_prompt(self, last_prompt: str) -> FakeChatResponse:
        # DfsTulipAgent uses this exact decomposition wording and expects an
        # empty subtask list so it proceeds to direct tool execution. If that
        # prompt is renamed or substantially rewritten, fail with this message
        # instead of silently returning the wrong plan.
        if "Decompose the following task into actionable subtasks" in last_prompt:
            if "What is 2+2?" in last_prompt:
                return self._text_response(json.dumps({"subtasks": []}))
            raise _unexpected_json_prompt(
                "DFS decomposition fake only supports `What is 2+2?`.",
                last_prompt,
            )

        # CotToolAgent and CotTulipAgent variants use generic JSON decomposition
        # prompts. This match is broad enough for small copy edits, but still
        # explicit about the only task the fake can plan.
        if _is_decomposition_prompt(last_prompt):
            if "What is 2+2?" in last_prompt or "`2+2`" in last_prompt:
                return self._text_response(
                    json.dumps({"subtasks": ["add two numbers"]})
                )
            raise _unexpected_json_prompt(
                "Decomposition fake only supports the simple `What is 2+2?` task.",
                last_prompt,
            )

        raise _unexpected_json_prompt(
            "No JSON fake response matched this prompt. If this prompt changed "
            "intentionally, update FakeChatClient._json_response_for_prompt.",
            last_prompt,
        )

    def _text_response(self, content: str) -> FakeChatResponse:
        return FakeChatResponse(
            choices=[FakeChoice(message=FakeMessage(content=content))],
            id=f"fake-chat-{len(self.calls)}",
            usage=FakeUsage(),
        )

    def _tool_response(self, name: str, arguments: dict[str, Any]) -> FakeChatResponse:
        self._tool_call_counter += 1
        return FakeChatResponse(
            choices=[
                FakeChoice(
                    message=FakeMessage(
                        content=None,
                        tool_calls=[
                            FakeToolCall(
                                id=f"fake-tool-call-{self._tool_call_counter}",
                                function=FakeFunctionCall(
                                    name=name,
                                    arguments=json.dumps(arguments),
                                ),
                            )
                        ],
                    )
                )
            ],
            id=f"fake-chat-{len(self.calls)}",
            usage=FakeUsage(),
        )


@pytest.fixture
def fake_embedding_client() -> FakeEmbeddingClient:
    return FakeEmbeddingClient()


@pytest.fixture
def fake_chat_client() -> FakeChatClient:
    return FakeChatClient()


@pytest.fixture
def tool_library_factory(
    tmp_path,
    fake_embedding_client: FakeEmbeddingClient,
) -> Callable[..., ToolLibrary]:
    def _factory(chroma_sub_dir: str = "library/", **kwargs: Any) -> ToolLibrary:
        return ToolLibrary(
            chroma_base_dir=f"{tmp_path}/",
            chroma_sub_dir=chroma_sub_dir,
            embedding_client=fake_embedding_client,
            **kwargs,
        )

    return _factory


def _semantic_embedding(text: str) -> list[float]:
    lower = text.lower()
    features = [
        ("add", "sum", "plus", "+", "addition"),
        ("subtract", "minus", "-", "difference"),
        ("multiply", "product", "*"),
        ("divide", "quotient", "/"),
        ("slow", "duration"),
        ("speak", "say", "loudly"),
        ("custom_division", "divisor"),
        ("ping", "pong"),
        ("alpha",),
        ("beta",),
    ]
    vector = [
        10.0 if any(keyword in lower for keyword in keywords) else 0.0
        for keywords in features
    ]
    vector.append(len(lower) / 1000.0)
    return vector


def _expects_json(params: dict[str, Any], last_prompt: str) -> bool:
    response_format = params.get("response_format")
    return (
        response_format == {"type": "json_object"} or "Return valid JSON" in last_prompt
    )


def _is_decomposition_prompt(prompt: str) -> bool:
    prompt_lower = prompt.lower()
    return (
        "necessary atomic actions" in prompt_lower
        or "necessary steps" in prompt_lower
        or "subtasks" in prompt_lower
    )


def _is_tool_search_prompt(prompt: str) -> bool:
    prompt_lower = prompt.lower()
    return (
        "search for appropriate tools" in prompt_lower
        or "search for suitable tools" in prompt_lower
    )


def _is_solve_with_tools_prompt(prompt: str) -> bool:
    prompt_lower = prompt.lower()
    return (
        "now use the tools" in prompt_lower
        or "solve the following task using exactly one" in prompt_lower
    )


def _is_simple_math_prompt(prompt: str) -> bool:
    return "2+2" in prompt or "2 + 2" in prompt


def _unexpected_fake_chat_request(
    reason: str, params: dict[str, Any]
) -> AssertionError:
    messages = params.get("messages", [])
    tools = params.get("tools") or []
    return AssertionError(
        "\n".join(
            [
                reason,
                f"Last prompt: {_last_message_content(messages)!r}",
                f"Available fake tools: {sorted(_tool_names(tools))}",
                (
                    "This usually means an agent prompt or test scenario changed "
                    "without updating FakeChatClient."
                ),
            ]
        )
    )


def _unexpected_json_prompt(reason: str, prompt: str) -> AssertionError:
    return AssertionError(
        "\n".join(
            [
                reason,
                f"JSON prompt: {prompt!r}",
                (
                    "This usually means a decomposition prompt changed without "
                    "updating FakeChatClient."
                ),
            ]
        )
    )


def _tool_names(tools: list[dict[str, Any]]) -> set[str]:
    return {tool["function"]["name"] for tool in tools}


def _last_message_content(messages: list[Any]) -> str:
    if not messages:
        return ""
    return _message_content(messages[-1])


def _all_message_content(messages: list[Any]) -> str:
    return "\n".join(_message_content(message) for message in messages)


def _message_content(message: Any) -> str:
    if isinstance(message, dict):
        return message.get("content") or ""
    return message.content or ""


def _tool_was_called(messages: list[Any], name: str) -> bool:
    return any(
        isinstance(message, dict)
        and message.get("role") == "tool"
        and message.get("name") == name
        for message in messages
    )
