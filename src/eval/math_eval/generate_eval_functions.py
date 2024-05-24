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
"""
Utility for generating Python math functions.
Must run reset_temp.py to generate empty temp module
"""
import ast
import importlib
import logging.config
import os.path
from inspect import getmembers, isfunction

import temp
import yaml
from black import FileMode, format_str
from openai import OpenAI, OpenAIError

from tulip_agent.constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE


# Set up logger
with open("logging_config.yaml", "rt") as log_config:
    config = yaml.safe_load(log_config.read())
logging.config.dictConfig(config)
logger = logging.getLogger("tool_generator")


MODULENAME = "temp"
FILENAME = MODULENAME + ".py"


SYSTEM_PROMPT = """\
You are a very senior Python developer.
You are extremely efficient and return ONLY code.
"""

TASK_PROMPT = """\
Please write NUMBER_FUNCTIONS Python functions for solving math tasks related to SUBFIELD.
You may include even trivial functions, such as addition and subtraction.
Adhere to the following rules:
1. Use sphinx documentation style without type documentation
2. Add meaningful and slightly verbose docstrings
3. Use python type hints
4. Return only valid code and avoid Markdown syntax for code blocks
5. Avoid adding examples to the docstring
"""

NO_DUPES_PROMPT = """\
Make sure to return unique functions and do not include the following ones: KNOWN_FUNCTIONS.
"""


def generate_functions(
    number_of_functions: int,
    subfield: str,
    known_functions: list[str],
    prompt: str = TASK_PROMPT,
    no_dupes: str = NO_DUPES_PROMPT,
    model: str = BASE_LANGUAGE_MODEL,
    temperature: float = BASE_TEMPERATURE,
):
    prompt = prompt.replace("NUMBER_FUNCTIONS", str(number_of_functions))
    prompt = prompt.replace("SUBFIELD", str(subfield))
    if known_functions:
        prompt += no_dupes.replace("KNOWN_FUNCTIONS", ", ".join(known_functions))
    logger.info(f"{prompt=}")

    openai_client = OpenAI()
    response = None
    while not response:
        try:
            response = openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=temperature,
            )
        except OpenAIError as e:
            logger.error(e)
    logger.info(
        f"Usage for {response.id} in tokens: "
        f"{response.usage.prompt_tokens} prompt and {response.usage.completion_tokens} completion."
    )
    return response.choices[0].message.content


def clean_generated_functions(functions: str):
    if functions.startswith("```"):
        functions = "\n".join(functions.split("\n")[1:-1])
    return functions


def append_to_file(functions: str, filename: str) -> None:
    formatted = format_str(functions, mode=FileMode())
    with open(filename, "a+") as f:
        f.write("\n\n" + formatted)


def check_existing_functions(modulename: str, filename: str) -> list:
    existing_functions = []
    if os.path.isfile(filename):
        importlib.reload(temp)
        existing_functions = [
            n for n, f in getmembers(temp, isfunction) if f.__module__ == modulename
        ]
    return existing_functions


def concat_files(sources: list[str], destination: str) -> None:
    with open(destination, "w") as d:
        for source in sources:
            with open(source) as s:
                for line in s:
                    d.write(line)


def check_if_valid_python(text: str) -> bool:
    try:
        ast.parse(text)
    except SyntaxError:
        return False
    return True


def generate(
    iterations: int,
    subfields: list[str],
    new_per_iteration: int = 5,
) -> None:
    for subfield in subfields:
        with open(FILENAME, "a+") as f:
            f.write(f"\n\n# {subfield}\n")
        for i in range(iterations):
            logger.info(f"{subfield} - iteration {i}")
            known_functions = check_existing_functions(
                modulename=MODULENAME, filename=FILENAME
            )
            logger.info(f"{known_functions=}")

            def _generate_and_clean(known):
                new_functions_ = generate_functions(
                    number_of_functions=new_per_iteration,
                    subfield=subfield,
                    known_functions=known,
                )
                new_functions_ = clean_generated_functions(functions=new_functions_)
                return new_functions_

            new_functions = _generate_and_clean(known_functions)
            while not check_if_valid_python(new_functions):
                logger.info("Generated code is invalid - retrying...")
                new_functions = _generate_and_clean(known_functions)

            logger.info(f"{new_functions=}")
            append_to_file(functions=new_functions, filename=FILENAME)
            updated_functions = check_existing_functions(
                modulename=MODULENAME, filename=FILENAME
            )
            logger.info(f"{updated_functions=}")
            logger.info(f"Now includes {len(updated_functions)} functions.")


if __name__ == "__main__":
    sfs = [
        "algebra",
        "analysis",
        "calculus",
        "number_theory",
        "geometry",
        "topology",
        "logic",
        "set_theory",
        "probability theory",
        "statistics",
    ]
    generate(iterations=25, subfields=sfs, new_per_iteration=5)
