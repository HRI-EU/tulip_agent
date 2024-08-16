#!/usr/bin/env python3
#
# Copyright (c) 2024, Honda Research Institute Europe GmbH
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#  this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in the
#  documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
from pathlib import Path
import json
import regex
import numpy as np
from latex2sympy2 import latex2sympy
import copy


def evaluate_latex_expression(latex_expression):
    try:
        # Parse the LaTeX expression
        expression = latex2sympy(latex_expression)
        # Evaluate the expression
        result = expression.evalf()
        all_returns = [str(expression),
                       str(float(str(result))),
                       str(float(str(result.round(4)))),
                       str(float(int(result * 10000))/10000),
                       str(float(str(result.round(2)))),
                       str(float(int(result * 100)) / 100)
                       ]
        return all_returns
    except Exception as e:
        print(f"Error evaluating expression: {e}")

def extract_nested_braces(content):
    pattern = r'\{(?:[^{}]++|(?R))*\}'
    matches = regex.findall(pattern, content)
    return matches

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
    level_counters = [0 for _ in [1,2,3,4,5]]
    for file_counter, file in enumerate(dir.glob('*.json')):
        if max_tasks and sum(level_counters) == max_tasks * len(levels):
            break
        content = json.loads(file.read_text())
        level_int = int(content["level"][-1])

        if level_int not in levels:
            continue
        if max_tasks and level_counters[level_int-1] == max_tasks:
            continue
        if "[asy]" in content["problem"]:
            continue

        level_counters[level_int-1] += 1

        # in the MATH files, the correct answer is marked with \boxed{ANSWER}
        print()
        extracted_solution = extract_nested_braces(content["solution"].split("boxed")[-1])
        print(extracted_solution)
        extracted_solution = extracted_solution[0][1:-1]
        print(extracted_solution)
        # print("Raw:", content["solution"])
        print("Extracted solution:", extracted_solution)

        solutions = [extracted_solution]
        # add fraction in clear format and as floating numbers
        if 'frac' in extracted_solution:
            evaluated = evaluate_latex_expression(extracted_solution)
            if evaluated:
                solutions.extend(evaluated)
            else:
                sp = extracted_solution.split("\\text")[0]
                evaluated = evaluate_latex_expression(sp)
                if evaluated:
                    solutions.extend(evaluated)


        # add numbers in different formant
        if "\!" in extracted_solution:
            stripped = copy.copy(extracted_solution).replace("\!", "")
            solutions.append(stripped)
            # solutions.append(copy.copy(extracted_solution).replace("\!", "").replace(",", "."))
            if "," in stripped:
                solutions.append(copy.copy(stripped).replace(",",""))

        # add dollar values without the dollar
        if "\$" in extracted_solution:
            solutions.append(copy.copy(extracted_solution).replace("\$", ""))

        # add percentages in different formats
        if "\%" in extracted_solution:
            solutions.append(copy.copy(extracted_solution).replace("\%", "%"))
        if "\\%" in extracted_solution:
            solutions.append(copy.copy(extracted_solution).replace("\\%", "%"))
        if "\%" in extracted_solution:
            solutions.append(copy.copy(extracted_solution).replace("\%", ""))
        if "\\%" in extracted_solution:
            solutions.append(copy.copy(extracted_solution).replace("\\%", ""))

        # add angles without angle
        if "^\\circ" in extracted_solution:
            solutions.append(copy.copy(extracted_solution).replace("^\\circ", ""))
        if "^{\\circ}" in extracted_solution:
            solutions.append(copy.copy(extracted_solution).replace("^{\\circ}", ""))

        # get numbers out of string
        if 'frac' not in extracted_solution:
            matches = regex.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", extracted_solution)
            if len(matches) == 1:
                solutions.extend(matches)

        # remove trailing zeros of numbers
        try:
            solutions.append(str(float(copy.copy(extracted_solution))))
        except:
            pass

        chars = ["+", "-"]
        if any(c in extracted_solution for c in chars):
            for c in chars:
                idx = extracted_solution.find(c)
                if idx > 0:
                    copied = copy.copy(extracted_solution)
                    copied = copied[:idx] + " " + copied[idx] + " " + copied[idx+1:]
                    solutions.append(copied)


        # remove \mbox
        if "\\mbox" in extracted_solution:
            removed = copy.copy(extracted_solution).replace("\\mbox{","")
            if removed[-1] == "}":
                removed = removed[:-1]
            solutions.append(removed)

        # add text without \text
        if "text{" in extracted_solution:
            removed = copy.copy(extracted_solution).replace("\\text{", "")
            if removed[-1] == "}":
                removed = removed[:-1]
            solutions.append(removed)

        new_solutions = []
        for sol in solutions:
            new_solutions.append(sol.strip())

            # add small numbers as words and vice versa if it's not a fraction answer
            if "frac" not in extracted_solution:
                if sol in ["1", "1.0"]:
                    new_solutions.append("one")
                if sol in ["2", "2.0"]:
                    new_solutions.append("two")
                if sol in ["3", "3.0"]:
                    new_solutions.append("three")
                if sol in ["4", "4.0"]:
                    new_solutions.append("four")
                if sol in ["5", "5.0"]:
                    new_solutions.append("five")
                if sol == "one":
                    new_solutions.append("1")
                if sol == "two":
                    new_solutions.append("2")
                if sol == "three":
                    new_solutions.append("3")
                if sol == "four":
                    new_solutions.append("4")
                if sol == "five":
                    new_solutions.append("5")

        solutions = list(set(new_solutions))
        print("All solutions:", solutions)
        # create task in tulips benchmark format
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
    if len(benchmark_tasks) > 0:
        with open(benchmark_task_file, "w") as file:
            json.dump(benchmark_tasks, file, indent=4)


if __name__ == "__main__":
    levels = [4,5]
    # levels = [1,2,3]
    create_benchmark_task(subcategory='prealgebra', levels=levels, max_tasks=None)
