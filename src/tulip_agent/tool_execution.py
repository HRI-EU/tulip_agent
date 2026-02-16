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
import concurrent.futures
import json
import logging
from dataclasses import dataclass
from typing import Any

from tulip_agent.tool import Tool


logger = logging.getLogger(__name__)


@dataclass
class ToolCallResult:
    value: str | None = None
    error: str | None = None


@dataclass
class Job:
    tool_call_id: str
    tool: Tool
    parameters: dict[str, Any]
    result: ToolCallResult | None = None


def execute_tool_calls(
    tool_calls: list, messages: list, tools: dict[str, Tool]
) -> None:
    if not tool_calls:
        return

    tool_messages = [{} for _ in tool_calls]
    valid_calls = []
    jobs = []

    for i, tool_call in enumerate(tool_calls):
        func_name = tool_call.function.name
        try:
            func_args = json.loads(tool_call.function.arguments)
        except json.decoder.JSONDecodeError as e:
            logger.error(e)
            generated_func_name, func_name = func_name, "invalid_tool_call"
            tool_call.function.name = func_name
            tool_call.function.arguments = "{}"
            function_response = (
                f"Error: Invalid arguments for {func_name} "
                f"(previously {generated_func_name}): {e}"
            )
            tool_messages[i] = {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": func_name,
                "content": function_response,
            }
            continue

        if func_name not in tools:
            logger.error(f"Invalid tool `{func_name}`.")
            generated_func_name, func_name = func_name, "invalid_tool_call"
            tool_call.function.name = func_name
            tool_call.function.arguments = "{}"
            function_response = (
                f"Error: {generated_func_name} is not a valid tool. "
                "Use only the tools available."
            )
            tool_messages[i] = {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": func_name,
                "content": function_response,
            }
            continue

        valid_calls.append((i, tool_call, func_name))
        jobs.append(
            Job(
                tool_call_id=tool_call.id,
                tool=tools[func_name],
                parameters=func_args,
            )
        )

    execution_results = execute_parallel_jobs(jobs=jobs)
    for (i, tool_call, func_name), execution_result in zip(
        valid_calls, execution_results
    ):
        if execution_result.result.error:
            logger.error(execution_result.result.error)
            function_response = execution_result.result.error
            tool_call.function.arguments = "{}"
        else:
            function_response = execution_result.result.value

        tool_messages[i] = {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": func_name,
            "content": str(function_response),
        }

    for tool_message, tool_call in zip(tool_messages, tool_calls):
        messages.append(tool_message)
        logger.info(
            (
                f"Function {tool_message['name']} returned `{tool_message['content']}` "
                f"for arguments {tool_call.function.arguments}."
            )
        )


def execute_parallel_jobs(jobs: list[Job]) -> list[Job]:
    if not jobs:
        return []

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs)) as executor:
        scheduled = []
        for job in jobs:
            try:
                fut = executor.submit(job.tool, **job.parameters)
                scheduled.append((job, fut))
            except TypeError as exc:
                job.result = ToolCallResult(error=f"Error: Invalid tool call - {exc}")
            except Exception as exc:
                job.result = ToolCallResult(
                    error=f"Error: Failed to schedule tool call - {exc}"
                )

        for job, fut in scheduled:
            try:
                if job.tool.timeout is None:
                    job.result = ToolCallResult(value=fut.result())
                else:
                    job.result = ToolCallResult(
                        value=fut.result(timeout=job.tool.timeout)
                    )
            except concurrent.futures.TimeoutError:
                error_message = (
                    job.tool.timeout_message
                    or "Tool call did not return a result before timeout."
                )
                job.result = ToolCallResult(error=f"Error: {error_message}")
            except Exception as exc:
                job.result = ToolCallResult(error=f"Error: Invalid tool call - {exc}")

    return jobs
