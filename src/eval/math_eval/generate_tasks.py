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
Generate tasks for math evaluation
"""
import importlib
import json
import logging.config
from inspect import getmembers, isfunction

import yaml
from openai import OpenAI, OpenAIError

from tulip_agent.constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE


# Set up agent loggers to save logs to file for analysis
with open("logging_config.yaml", "rt") as log_config:
    config = yaml.safe_load(log_config.read())
logging.config.dictConfig(config)
logger = logging.getLogger("task_generator")


SYSTEM_PROMPT = """\
You are an expert mathematician.
Your task is to come up with math tasks of varying difficulty.
"""


TASK_PROMPT = """\
Come up with a math problem posed as a text question the result of which is a single value.
{explanation}
The problem must be solvable with the following functions:
{functions}
Do not include formulas in the question.
Return valid JSON in the following form:
{{
    "task": "Description of the task",
    "functions": [
        "necessary_function",
    ]
}}
Make sure to create a new task that is not in the following list:
{known_tasks}
"""


DIFFICULTY_EXPLANATIONS = {
    "easy": "The task must require using exactly one function.",
    "medium": "The task must require using two or three functions.",
    "hard": "The task must require using at least four functions.",
}


def generate_tasks(
    number_of_tasks_each: int,
    function_module,
    difficulties: list[str] = ("easy", "medium", "hard"),
    model: str = BASE_LANGUAGE_MODEL,
    temperature: float = BASE_TEMPERATURE,
) -> list:
    openai_client = OpenAI()

    function_module = importlib.import_module(function_module)
    function_names = [
        n
        for n, f in getmembers(function_module, isfunction)
        if f.__module__ == function_module.__name__
    ]

    res = []
    for difficulty in difficulties:
        known_tasks = []
        for i in range(number_of_tasks_each):
            prompt = TASK_PROMPT.format(
                number=number_of_tasks_each,
                explanation=DIFFICULTY_EXPLANATIONS[difficulty],
                functions=", ".join(function_names),
                known_tasks=known_tasks,
            )

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
                        response_format={"type": "json_object"},
                    )
                except OpenAIError as e:
                    logger.error(e)
            res_ = json.loads(response.choices[0].message.content)
            res_["name"] = "M.T." + difficulty[0].upper() + f".{i:03d}"
            res_["valid_solutions"] = [""]
            res.append(res_)
            known_tasks.append(res_["task"])
            logger.info(f"{res_=}")
    return res


def write_tasks_to_file(
    task_data: list,
    task_file: str = "math_tasks_generated.json",
):
    with open(task_file, "w") as f:
        json.dump(task_data, f, indent=4)


if __name__ == "__main__":
    tasks = generate_tasks(
        number_of_tasks_each=20,
        function_module="math_tools",
    )
    write_tasks_to_file(tasks)
