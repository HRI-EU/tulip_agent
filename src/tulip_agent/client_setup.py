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
import logging
import os
from enum import Enum
from pathlib import Path

from openai import AzureOpenAI, OpenAI

from tulip_agent.constants import (
    BASE_EMBEDDING_MODEL,
    BASE_LANGUAGE_MODEL,
    BASE_REASONING_MODEL,
    BASE_TEMPERATURE,
)


logger = logging.getLogger(__name__)


class ModelServeMode(Enum):
    AZURE = "azure"
    OAI_COMPATIBLE = "oai_compatible"
    OPENAI = "openai"


DOTENV_PATH = Path(".env")
MODEL_SERVE_MODE_ENV = "TULIP_MODEL_SERVE_MODE"
BASE_MODEL_ENV = "TULIP_BASE_MODEL"
REASONING_MODEL_ENV = "TULIP_REASONING_MODEL"
EMBEDDING_MODEL_ENV = "TULIP_EMBEDDING_MODEL"


def load_dotenv(dotenv_path: Path | str | None = None) -> None:
    """Load simple KEY=value settings from project-root .env.

    The loader is deliberately small: it supports the common .env shape used by
    the examples, never overrides already exported variables, and avoids adding a
    runtime dependency just to select a model provider.
    """
    path = _find_dotenv(dotenv_path)
    if path is None:
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def _find_dotenv(dotenv_path: Path | str | None = None) -> Path | None:
    """Return the .env file Tulip should use, without searching arbitrary paths."""
    if dotenv_path is not None:
        path = Path(dotenv_path)
        return path if path.exists() else None

    # Prefer the process cwd for normal `uv run examples/...` usage. Fall back to
    # the editable-source project root so absolute example launches still work.
    candidates = [
        DOTENV_PATH,
        Path(__file__).resolve().parents[2] / ".env",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def check_for_environment_variable(env_var: str) -> None:
    if env_var not in os.environ:
        raise ValueError(f"{env_var} not set.")


def resolve_model_serve_mode(
    model_serve_mode: ModelServeMode | str | None = None,
) -> ModelServeMode:
    """Resolve the provider from explicit input, .env, or exported variables."""
    load_dotenv()

    if model_serve_mode is not None:
        return _coerce_model_serve_mode(model_serve_mode)

    configured_mode = os.getenv(MODEL_SERVE_MODE_ENV)
    if configured_mode:
        return _coerce_model_serve_mode(configured_mode)

    candidates = []
    if os.getenv("OPENAI_API_KEY"):
        candidates.append(ModelServeMode.OPENAI)
    if all(
        os.getenv(name)
        for name in (
            "AZURE_OPENAI_API_KEY",
            "AZURE_API_VERSION",
            "AZURE_OPENAI_ENDPOINT",
        )
    ):
        candidates.append(ModelServeMode.AZURE)
    if os.getenv("OAI_COMPATIBLE_BASE_URL"):
        candidates.append(ModelServeMode.OAI_COMPATIBLE)

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        modes = ", ".join(mode.value for mode in candidates)
        raise ValueError(
            "Multiple Tulip model providers are configured "
            f"({modes}). Set TULIP_MODEL_SERVE_MODE to one of: "
            "openai, azure, oai_compatible."
        )
    raise ValueError(
        "No Tulip model provider configured. Add ./.env or export variables for "
        "one provider, for example "
        "TULIP_MODEL_SERVE_MODE=oai_compatible, "
        "TULIP_BASE_MODEL=<chat-model>, "
        "TULIP_EMBEDDING_MODEL=<embedding-model>, and "
        "OAI_COMPATIBLE_BASE_URL=<base-url>."
    )


def resolve_base_model(
    *,
    required: bool = True,
    fallback_to_legacy_default: bool = False,
) -> str | None:
    return _resolve_model_name(
        env_var=BASE_MODEL_ENV,
        label="base chat model",
        required=required,
        legacy_default=BASE_LANGUAGE_MODEL if fallback_to_legacy_default else None,
    )


def resolve_reasoning_model(
    *,
    fallback_to_legacy_default: bool = False,
) -> str | None:
    return _resolve_model_name(
        env_var=REASONING_MODEL_ENV,
        label="reasoning model",
        required=False,
        legacy_default=BASE_REASONING_MODEL if fallback_to_legacy_default else None,
    )


def resolve_embedding_model(
    *,
    required: bool = True,
    fallback_to_legacy_default: bool = False,
) -> str | None:
    return _resolve_model_name(
        env_var=EMBEDDING_MODEL_ENV,
        label="embedding model",
        required=required,
        legacy_default=BASE_EMBEDDING_MODEL if fallback_to_legacy_default else None,
    )


def resolve_temperature(temperature: float | None) -> float:
    return BASE_TEMPERATURE if temperature is None else temperature


def create_client(
    model_serve_mode: ModelServeMode | str | None = None,
    timeout: int = 60,
    max_retries: int = 10,
) -> AzureOpenAI | OpenAI:
    mode = resolve_model_serve_mode(model_serve_mode)
    match mode:
        case ModelServeMode.OPENAI:
            check_for_environment_variable("OPENAI_API_KEY")
            client = OpenAI(
                timeout=timeout,
                max_retries=max_retries,
            )
        case ModelServeMode.OAI_COMPATIBLE:
            check_for_environment_variable("OAI_COMPATIBLE_BASE_URL")
            client = OpenAI(
                base_url=os.getenv("OAI_COMPATIBLE_BASE_URL"),
                api_key=os.getenv("OAI_COMPATIBLE_API_KEY", "EMPTY"),
                timeout=timeout,
                max_retries=max_retries,
            )
        case ModelServeMode.AZURE:
            check_for_environment_variable("AZURE_OPENAI_API_KEY")
            check_for_environment_variable("AZURE_API_VERSION")
            check_for_environment_variable("AZURE_OPENAI_ENDPOINT")
            client = AzureOpenAI(
                api_version=os.getenv("AZURE_API_VERSION"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                timeout=timeout,
                max_retries=max_retries,
            )
        case _:
            raise ValueError(f"Unexpected model_serve_mode: {mode}.")
    return client


def _coerce_model_serve_mode(model_serve_mode: ModelServeMode | str) -> ModelServeMode:
    if isinstance(model_serve_mode, ModelServeMode):
        return model_serve_mode
    try:
        return ModelServeMode(model_serve_mode.strip().lower())
    except ValueError as exc:
        raise ValueError(
            f"Unexpected model serve mode {model_serve_mode!r}. "
            "Expected one of: openai, azure, oai_compatible."
        ) from exc


def _resolve_model_name(
    *,
    env_var: str,
    label: str,
    required: bool,
    legacy_default: str | None,
) -> str | None:
    load_dotenv()
    configured_model = os.getenv(env_var)
    if configured_model:
        return configured_model
    if legacy_default:
        return legacy_default
    if required:
        raise ValueError(
            f"No Tulip {label} configured. Set {env_var} in ./.env or pass the "
            "model explicitly to the agent/tool library constructor."
        )
    return None
