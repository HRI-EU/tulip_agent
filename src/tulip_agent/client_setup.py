#!/usr/bin/env python3
#
# Copyright (c) 2024, Honda Research Institute Europe GmbH
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import logging
import os
from enum import Enum

from openai import AzureOpenAI, OpenAI


logger = logging.getLogger(__name__)


class ModelServeMode(Enum):
    AZURE = "azure"
    OAI_COMPATIBLE = "oai_compatible"
    OPENAI = "openai"


def check_for_environment_variable(env_var: str) -> None:
    if env_var not in os.environ:
        raise ValueError(f"{env_var} not set.")


def create_client(model_serve_mode: ModelServeMode) -> AzureOpenAI | OpenAI:
    match model_serve_mode:
        case ModelServeMode.OPENAI:
            check_for_environment_variable("OPENAI_API_KEY")
            client = OpenAI(
                timeout=60,
                max_retries=10,
            )
        case ModelServeMode.OAI_COMPATIBLE:
            check_for_environment_variable("OAI_COMPATIBLE_BASE_URL")
            check_for_environment_variable("OAI_COMPATIBLE_API_KEY")
            client = OpenAI(
                base_url=os.getenv("OAI_COMPATIBLE_BASE_URL"),
                api_key=os.getenv("OAI_COMPATIBLE_API_KEY"),
                timeout=60,
                max_retries=10,
            )
        case ModelServeMode.AZURE:
            check_for_environment_variable("AZURE_OPENAI_API_KEY")
            check_for_environment_variable("AZURE_API_VERSION")
            check_for_environment_variable("AZURE_OPENAI_ENDPOINT")
            client = AzureOpenAI(
                api_version=os.getenv("AZURE_API_VERSION"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                timeout=60,
                max_retries=10,
            )
        case _:
            raise ValueError(f"Unexpected model_serve_mode: {model_serve_mode}.")
    return client
