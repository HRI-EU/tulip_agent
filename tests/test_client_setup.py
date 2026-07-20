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

import tulip_agent.client_setup as client_setup
from tulip_agent.client_setup import (
    create_client,
    load_dotenv,
    resolve_base_model,
    resolve_embedding_model,
    resolve_model_serve_mode,
)


CONFIG_ENV_VARS = [
    "TULIP_MODEL_SERVE_MODE",
    "TULIP_BASE_MODEL",
    "TULIP_REASONING_MODEL",
    "TULIP_EMBEDDING_MODEL",
    "OPENAI_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "AZURE_API_VERSION",
    "AZURE_OPENAI_ENDPOINT",
    "OAI_COMPATIBLE_BASE_URL",
    "OAI_COMPATIBLE_API_KEY",
]


def test_load_dotenv_from_project_root_without_overriding_existing_env(
    monkeypatch,
    tmp_path,
):
    _clear_config_env(monkeypatch)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("TULIP_BASE_MODEL", "exported-model")
    tmp_path.joinpath(".env").write_text(
        "TULIP_BASE_MODEL=file-model\nTULIP_EMBEDDING_MODEL=file-embedding\n",
        encoding="utf-8",
    )

    load_dotenv()

    assert resolve_base_model() == "exported-model"
    assert resolve_embedding_model() == "file-embedding"


def test_load_dotenv_explicit_path_uses_repo_env_when_cwd_differs(
    monkeypatch,
    tmp_path,
):
    _clear_config_env(monkeypatch)
    run_dir = tmp_path / "run-from-here"
    run_dir.mkdir()
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    project_dir.joinpath(".env").write_text(
        "TULIP_BASE_MODEL=file-model\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(run_dir)

    load_dotenv(project_dir / ".env")

    assert resolve_base_model() == "file-model"


def test_load_dotenv_falls_back_to_editable_project_root(monkeypatch, tmp_path):
    _clear_config_env(monkeypatch)
    run_dir = tmp_path / "run-from-here"
    run_dir.mkdir()
    project_dir = tmp_path / "project"
    package_dir = project_dir / "src" / "tulip_agent"
    package_dir.mkdir(parents=True)
    project_dir.joinpath(".env").write_text(
        "TULIP_BASE_MODEL=repo-root-model\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(run_dir)
    monkeypatch.setattr(
        client_setup,
        "__file__",
        str(package_dir / "client_setup.py"),
    )

    load_dotenv()

    assert resolve_base_model() == "repo-root-model"


def test_create_client_uses_oai_compatible_env_with_empty_key(monkeypatch, tmp_path):
    _clear_config_env(monkeypatch)
    monkeypatch.chdir(tmp_path)
    tmp_path.joinpath(".env").write_text(
        "\n".join(
            [
                "TULIP_MODEL_SERVE_MODE=oai_compatible",
                "OAI_COMPATIBLE_BASE_URL=http://localhost:11434/v1",
            ]
        ),
        encoding="utf-8",
    )

    client = create_client()

    assert client.api_key == "EMPTY"
    assert str(client.base_url) == "http://localhost:11434/v1/"


def test_provider_can_be_inferred_from_single_configured_endpoint(
    monkeypatch,
    tmp_path,
):
    _clear_config_env(monkeypatch)
    monkeypatch.chdir(tmp_path)
    tmp_path.joinpath(".env").write_text("", encoding="utf-8")
    monkeypatch.setenv("OAI_COMPATIBLE_BASE_URL", "http://localhost:11434/v1")

    assert resolve_model_serve_mode().value == "oai_compatible"


def test_missing_provider_fails_with_configuration_hint(monkeypatch, tmp_path):
    _clear_config_env(monkeypatch)
    monkeypatch.chdir(tmp_path)
    tmp_path.joinpath(".env").write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="No Tulip model provider configured"):
        create_client()


def test_ambiguous_provider_configuration_requires_explicit_mode(
    monkeypatch,
    tmp_path,
):
    _clear_config_env(monkeypatch)
    monkeypatch.chdir(tmp_path)
    tmp_path.joinpath(".env").write_text("", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-key")
    monkeypatch.setenv("OAI_COMPATIBLE_BASE_URL", "http://localhost:11434/v1")

    with pytest.raises(ValueError, match="Multiple Tulip model providers"):
        resolve_model_serve_mode()


def _clear_config_env(monkeypatch):
    for env_var in CONFIG_ENV_VARS:
        monkeypatch.delenv(env_var, raising=False)
