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
from dataclasses import dataclass
from typing import Any

from tulip_agent.tool import Tool


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


def execute_tool_calls(jobs: list[Job]) -> list[Job]:
    if not jobs:
        return []

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs)) as executor:
        scheduled = []
        for job in jobs:
            try:
                fut = executor.submit(job.tool.execute, **job.parameters)
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
            except concurrent.futures.TimeoutError as exc:
                error_message = (
                    job.tool.timeout_message
                    or "Tool call did not return a result before timeout"
                )
                job.result = ToolCallResult(error=f"Error: {error_message} - {exc}")
            except Exception as exc:
                job.result = ToolCallResult(error=f"Error: Invalid tool call - {exc}")

    return jobs
