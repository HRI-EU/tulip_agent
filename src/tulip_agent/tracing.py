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
from __future__ import annotations

import importlib
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import Any, Callable


logger = logging.getLogger(__name__)

_weave_module = None
_weave_client = None
_init_attempted = False
_trace_inputs = False
_init_lock = Lock()


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _sanitize_value(value: Any, max_length: int = 500) -> Any:
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return value[:max_length]
    if isinstance(value, dict):
        return {str(k): _sanitize_value(v, max_length) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_sanitize_value(item, max_length) for item in value]
    for attr in ("unique_id", "function_name", "__name__"):
        val = getattr(value, attr, None)
        if val is not None:
            return val
    return type(value).__name__


def _maybe_capture_inputs(inputs: dict[str, Any] | None) -> dict[str, Any]:
    if not inputs:
        return {}
    if _trace_inputs:
        return _sanitize_value(inputs)
    return {"redacted": True, "keys": sorted(str(k) for k in inputs)}


def _get_message_attr(message: Any, key: str, default: Any = None) -> Any:
    if isinstance(message, dict):
        return message.get(key, default)
    return getattr(message, key, default)


def summarize_messages(
    messages: list[dict[str, Any]] | None,
    include_content: bool = False,
) -> list[dict[str, Any]]:
    if not messages:
        return []
    summaries = []
    for msg in messages:
        summary = {"role": _get_message_attr(msg, "role")}
        for key in ("name", "tool_call_id"):
            val = _get_message_attr(msg, key)
            if val is not None:
                summary[key] = val
        content = _get_message_attr(msg, "content")
        if include_content:
            summary["content"] = _sanitize_value(content)
        elif content is not None:
            summary["content_preview"] = _sanitize_value(str(content), 120)
        summaries.append(summary)
    return summaries


def summarize_response(response: Any) -> dict[str, Any]:
    if response is None:
        return {"response": None}

    choices = getattr(response, "choices", None) or []
    first_choice = choices[0] if choices else None
    message = getattr(first_choice, "message", None)
    tool_calls = getattr(message, "tool_calls", None) or []
    usage = getattr(response, "usage", None)

    return {
        "id": getattr(response, "id", None),
        "model": getattr(response, "model", None),
        "finish_reason": getattr(first_choice, "finish_reason", None),
        "tool_call_count": len(tool_calls),
        "content_preview": _sanitize_value(getattr(message, "content", None), 200),
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
    }


def init_weave(
    project_name: str | None = None,
    *,
    trace_inputs: bool | None = None,
) -> bool:
    global _weave_client, _init_attempted, _weave_module, _trace_inputs

    if _weave_client is not None:
        return True
    if _init_attempted:
        return False

    project = project_name or os.getenv("TULIP_WEAVE_PROJECT")
    if not project:
        return False

    if trace_inputs is None:
        trace_inputs = _env_flag("TULIP_WEAVE_TRACE_INPUTS")
    _trace_inputs = trace_inputs

    with _init_lock:
        if _weave_client is not None:
            return True
        if _init_attempted:
            return False
        _init_attempted = True
        try:
            wandb = importlib.import_module("wandb")
            api_key = os.getenv("WANDB_API_KEY")
            if api_key:
                wandb.login(key=api_key)
            _weave_module = importlib.import_module("weave")
            _weave_module.init(project)
            _weave_client = _weave_module.get_client()
            logger.info("Initialized Weave tracing for project `%s`.", project)
        except ModuleNotFoundError:
            logger.warning(
                "Weave tracing enabled but `weave` or `wandb` package is not installed."
            )
            _weave_module = None
            return False
        except Exception as exc:
            logger.warning("Failed to initialize Weave tracing: %s", exc)
            _weave_module = None
            return False
    return True


def weave_tracing_enabled() -> bool:
    return _weave_client is not None


def get_thread_pool_executor() -> type[ThreadPoolExecutor]:
    if _weave_client is not None and hasattr(_weave_module, "ThreadPoolExecutor"):
        return _weave_module.ThreadPoolExecutor
    return ThreadPoolExecutor


def trace_call(
    op_name: str,
    fn: Callable[[], Any],
    *,
    inputs: dict[str, Any] | None = None,
    attributes: dict[str, Any] | None = None,
    output_summarizer: Callable[[Any], Any] | None = None,
) -> Any:
    if _weave_client is None:
        return fn()

    call = _weave_client.create_call(
        op=op_name,
        inputs=_maybe_capture_inputs(inputs),
        attributes=_sanitize_value(attributes or {}),
    )
    try:
        result = fn()
    except Exception as exc:
        _weave_client.finish_call(call, exception=exc)
        raise

    output = output_summarizer(result) if output_summarizer else _sanitize_value(result)
    _weave_client.finish_call(call, output=output)
    return result


def finish_weave() -> None:
    if _weave_module is not None and hasattr(_weave_module, "finish"):
        _weave_module.finish()


def reset_weave_state() -> None:
    global _weave_module, _weave_client, _init_attempted, _trace_inputs

    _weave_module = None
    _weave_client = None
    _init_attempted = False
    _trace_inputs = False
