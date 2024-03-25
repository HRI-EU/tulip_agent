#!/usr/bin/env python3
"""
Utility for generating Python math functions.
Must run reset_temp.py to generate empty temp module
"""
import logging.config
import os.path
import yaml

from black import format_str, FileMode
import importlib
from inspect import getmembers, isfunction
from openai import OpenAI, OpenAIError

from constants import BASE_LANGUAGE_MODEL, BASE_TEMPERATURE
import temp


# Set up logger
with open("logging_config.yaml", "rt") as log_config:
    config = yaml.safe_load(log_config.read())
logging.config.dictConfig(config)
logger = logging.getLogger("tool_generator")


SYSTEM_PROMPT = """\
You are a very senior Python developer.
You are extremely efficient and return ONLY code.
"""

TASK_PROMPT = """\
Please write NUMBER_FUNCTIONS Python functions for solving math tasks, e.g., add or subtract.
Adhere to the following rules:
1. Use sphinx documentation style without type documentation
2. Add meaningful and slightly verbose docstrings
3. Use python type hints
4. Avoid adding examples to the docstring
"""

NO_DUPES_PROMPT = """\
Make sure return unique functions and do not include the following ones: KNOWN_FUNCTIONS.
"""


def generate_functions(
    number_of_functions: int,
    known_functions: list[str],
    prompt: str = TASK_PROMPT,
    no_dupes: str = NO_DUPES_PROMPT,
    model: str = BASE_LANGUAGE_MODEL,
    temperature: float = BASE_TEMPERATURE,
):
    prompt = prompt.replace("NUMBER_FUNCTIONS", str(number_of_functions))
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


def generate(iterations: int) -> None:
    for i in range(iterations):
        logger.info(f"Iteration {i}")
        known_functions = check_existing_functions(
            modulename=modulename, filename=filename
        )
        logger.info(f"{known_functions=}")
        new_functions = generate_functions(
            number_of_functions=5, known_functions=known_functions
        )
        new_functions = clean_generated_functions(functions=new_functions)
        logger.info(f"{new_functions=}")
        append_to_file(functions=new_functions, filename=filename)
        updated_functions = check_existing_functions(
            modulename=modulename, filename=filename
        )
        logger.info(f"{updated_functions=}")
        logger.info(f"Now includes {len(updated_functions)} functions.")


if __name__ == "__main__":
    modulename = "temp"
    filename = modulename + ".py"
    generate(iterations=20)
