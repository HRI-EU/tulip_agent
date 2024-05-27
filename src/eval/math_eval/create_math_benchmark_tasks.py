#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ***DESCRIPTION***.
#
#  Copyright (C)
#  Honda Research Institute Europe GmbH
#  Carl-Legien-Str. 30
#  63073 Offenbach/Main
#  Germany
#
#  UNPUBLISHED PROPRIETARY MATERIAL.
#  ALL RIGHTS RESERVED.
#
#

import os
from pathlib import Path
import json
import re

def create_benchmark_task(subcategory, level, max_tasks=None):
    """
    Creat TULIP eval compatible .json from the MATH benchmark tasks.

    :param subcategory:  the category of tasks from MATH.
    :param level:  the level of the tasks from MATH.
    :param max_tasks:  maximal number of tasks create. (default=None creates all available)
    :return: None
    """

    suffix = ""
    if max_tasks:
        suffix = f"_{max_tasks}_tasks"
    benchmark_task_file = f"MATH_benchmarks/benchmark_{subcategory}_{level}{suffix}.json"

    cwd = Path.cwd()
    path = os.path.join(Path(cwd).parents[2], f"data/MATH/train/{subcategory}")
    dir = Path(path)

    benchmark_tasks = []
    for file_counter, file in enumerate(dir.glob('*.json')):
        if max_tasks and len(benchmark_tasks) == max_tasks:
            break
        content = json.loads(file.read_text())
        if content["level"] != f"Level {level}":
            continue

        # print(file.name)
        # print("Problem:\n", content["problem"])
        # print("Answer:")
        # for sent in content["solution"].split(". "):
        #     print(sent)

        # in the MATH files, the correct answer is marked with \boxed{ANSWER}
        extracted_solution = re.search('boxed{(.+?)}', content["solution"]).group(1)
        # print("Extracted solution:", extracted_solution)

        # create task in tulips benchmark format
        solutions = [extracted_solution]
        new_task = {
            "task": content["problem"],
            "raw_solution": content["solution"],
            "functions": [],
            "name": f"{subcategory}.{file.name.split('.')[0]}.{level}",
            "category": subcategory,
            "level": level,
            "valid_solutions": solutions
        }
        benchmark_tasks.append(new_task)

    print(f"Created {len(benchmark_tasks)} from '{subcategory}' Level '{level}', saving to '{benchmark_task_file}'")
    if len(benchmark_tasks) > 0:
        with open(benchmark_task_file, "w") as file:
            json.dump(benchmark_tasks, file, indent=4)


if __name__ == "__main__":
    for level in range(1,6):
        create_benchmark_task(subcategory='prealgebra', level=level, max_tasks=None)
