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

def create_benchmark_task(subcategory, levels, max_tasks=None):
    """
    Creat TULIP eval compatible .json from the MATH benchmark tasks.

    :param subcategory:  the category of tasks from MATH.
    :param levels:  list of levels of the tasks from MATH.
    :param max_tasks:  maximal number of tasks create. (default=None creates all available)
    :return: None
    """

    suffix = ""
    if max_tasks:
        suffix = f"_{max_tasks}_tasks"
    benchmark_task_file = f"MATH_benchmarks/benchmark_{subcategory}_{levels[0]}-{levels[-1]}{suffix}.json"

    cwd = Path.cwd()
    path = os.path.join(Path(cwd).parents[2], f"data/MATH/train/{subcategory}")
    dir = Path(path)

    benchmark_tasks = []
    level_counters = [0 for _ in levels]
    for file_counter, file in enumerate(dir.glob('*.json')):
        if max_tasks and sum(level_counters) == max_tasks * len(levels):
            break
        content = json.loads(file.read_text())
        level_int = int(content["level"][-1])

        if level_int not in levels:
            continue
        if max_tasks and level_counters[level_int-1] == max_tasks:
            continue

        level_counters[level_int-1] += 1


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
            "name": f"{subcategory}.{file.name.split('.')[0]}.{level_int}",
            "category": subcategory,
            "level": level_int,
            "valid_solutions": solutions
        }
        benchmark_tasks.append(new_task)

    print(level_counters)
    print(f"Created {len(benchmark_tasks)} from '{subcategory}' Levels '{levels}', saving to '{benchmark_task_file}'")
    # if len(benchmark_tasks) > 0:
    #     with open(benchmark_task_file, "w") as file:
    #         json.dump(benchmark_tasks, file, indent=4)


if __name__ == "__main__":
    levels = [1,2,3,4,5]
    create_benchmark_task(subcategory='prealgebra', levels=levels, max_tasks=None)
