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
import ast
import importlib
import json
import logging.config
import math
import os
import re
import shutil
import statistics
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from inspect import getmembers, isfunction
from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import pandas as pd
import seaborn as sns
import tiktoken
import yaml

from tulip_agent.function_analyzer import FunctionAnalyzer


# Set up logger
with open("logging_config.yaml", "rt") as log_config:
    config = yaml.safe_load(log_config.read())
logging.config.dictConfig(config)
logger = logging.getLogger("result_analysis")


# source: https://openai.com/pricing, all in dollars
OAI_PRICES = {
    "gpt-3.5-turbo-0125": {
        "input": 0.5 / 1_000_000,
        "output": 1.5 / 1_000_000,
    },
    "gpt-4-turbo-2024-04-09": {
        "input": 10 / 1_000_000,
        "output": 30 / 1_000_000,
    },
    "gpt-4o-2024-05-13": {
        "input": 5 / 1_000_000,
        "output": 15 / 1_000_000,
    },
    "text-embedding-ada-002": 0.1 / 1_000_000,
    "text-embedding-3-small": 0.02 / 1_000_000,
    "text-embedding-3-large": 0.13 / 1_000_000,
}


@dataclass
class ToolCall:
    name: str
    arguments: dict
    result: str


@dataclass
class Result:
    agent: str
    task: str
    model: str
    embedding_model: str
    input_tokens: int
    completion_tokens: int
    embedding_tokens: int
    tools_called: list[ToolCall]
    response: str
    ground_truth: Optional[list[str]] = None
    costs: Optional[float] = None
    function_precision: Optional[float] = None
    function_recall: Optional[float] = None
    correctness: Optional[bool] = None

    def __post_init__(self) -> None:
        self.costs = round(
            (
                OAI_PRICES[self.model]["input"] * self.input_tokens
                + OAI_PRICES[self.model]["output"] * self.completion_tokens
                + OAI_PRICES[self.embedding_model] * self.embedding_tokens
            ),
            5,
        )


def interquartile_mean(values: list) -> float:
    lnv = len(values)
    q = lnv // 4
    if q == 0:
        return 0.
    if lnv % 4 == 0:
        nums = values[q:-q]
        return sum(nums) / (2 * q)
    else:
        q_ = lnv / 4
        w = q + 1 - q_
        nums = [values[q] * w] + values[q + 1 : -(q + 1)] + [values[-(q + 1)] * w]
        return sum(nums) / (2 * q_)


def extract_data_from_log(
    log_file: str, model: str, embedding_model: str
) -> list[Result]:
    results = []
    tool_library_costs = calc_costs_for_tool_library()
    with open(log_file, "r") as f:
        logs = f.read()
    parts, current = [], []
    for log_message in logs.strip().split("\n2024-"):
        current.append(log_message)
        if "returns response" in log_message:
            parts.append(current)
            current = []
        # handle cases without a response log
        if len(current) > 1 and "received query: " in log_message:
            current.pop()
            parts.append(current)
            current = [log_message]
    for p in parts:
        agent = p[0].split(" - INFO - ")[-1].split()[0]
        query = p[0].split("received query: ")[-1]
        response = p[-1].split("returns response: ")[-1]
        in_tokens, out_tokens, embed_tokens = 0, 0, 0
        tools_called = []
        for log_line in p[1:-1]:
            if "Usage for chatcmpl-" in log_line:
                token_counts = log_line.split(" in tokens: ")[-1].split(" completion.")[
                    0
                ]
                i, o = token_counts.split(" prompt and ")
                in_tokens += int(i)
                out_tokens += int(o)
            elif "Usage for embedding in tokens" in log_line:
                embed_tokens += int(
                    log_line.split("Usage for embedding in tokens: ")[-1].split(
                        " prompt."
                    )[0]
                )
            elif all(w in log_line for w in ("Function", "returned", "for arguments")):
                tool_name = (
                    log_line.split(" - INFO - Function ")[-1].split()[0].split("__")[-1]
                )
                tool_result = (
                    log_line.split(" - INFO - Function ")[-1]
                    .split()[2]
                    .replace("`", "")
                )
                tool_arguments = json.loads(log_line.split(" for arguments ")[-1][:-1])
                tools_called.append(
                    ToolCall(
                        name=tool_name, arguments=tool_arguments, result=tool_result
                    )
                )
        if agent in (
            "MinimalTulipAgent",
            "NaiveTulipAgent",
            "CotTulipAgent",
            "AutoTulipAgent",
        ):
            embed_tokens += tool_library_costs
        r = Result(
            agent=agent,
            task=query,
            model=model,
            embedding_model=embedding_model,
            input_tokens=in_tokens,
            completion_tokens=out_tokens,
            embedding_tokens=embed_tokens,
            tools_called=tools_called,
            response=response,
        )
        results.append(r)
        # logger.info(f"Retrieved data for {r.agent} on `{r.task}`.")
    return results


def calc_costs_for_tool_library(settings_file: str = "math_eval_settings.yaml"):
    with open(settings_file, "rt") as mes_:
        settings_ = yaml.safe_load(mes_.read())
    tools_filename = settings_["tools"]
    tools = importlib.import_module(tools_filename)

    fa = FunctionAnalyzer()

    functions = [
        getattr(tools, n)
        for n, f in getmembers(tools, isfunction)
        if f.__module__ == tools.__name__
    ]

    docstrings = [fa.analyze_function(f)["function"]["description"] for f in functions]
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = sum([len(encoding.encode(ds)) for ds in docstrings])
    return num_tokens


def assess_data(
    results: list[Result], ground_truth: str
) -> tuple[list[Result], dict[str, str]]:
    with open(ground_truth, "r") as gtf:
        gtf_data_ = json.load(gtf)
        gtf_data = {e["task"]: e for e in gtf_data_}
    for r in results:
        # logger.info(f"Assessing {r.agent} on `{r.task}`.")
        if r.task not in gtf_data:
            logger.warning(f"No ground truth found for {r.task}")
            continue
        r.ground_truth = [str(vs) for vs in gtf_data[r.task]["valid_solutions"]]

        # try:
        #     answer_string = r.response.split("<result>")[-1]
        # except:
        #     print(f"-------- NO <RESULT> {r.agent}\n{answer_string}")
        answer_string = r.response
        r.correctness = any(
            str(vs) in answer_string for vs in gtf_data[r.task]["valid_solutions"]
        )
        tool_call_names = [t.name for t in r.tools_called]
        relevant_tools = list(
            (
                Counter(tool_call_names) & Counter(gtf_data[r.task]["functions"])
            ).elements()
        )
        r.function_precision = (
            len(relevant_tools) / len(tool_call_names) if tool_call_names else 0.0
        )
        if len(gtf_data[r.task]["functions"]) > 0:
            r.function_recall = len(relevant_tools) / len(gtf_data[r.task]["functions"])
        else:
            r.function_recall = 0.0
    return results, {k: gtf_data[k]["name"] for k in gtf_data}


def add_linebreak(label: str) -> str:
    if len(label) > 12 and len(label.split()) > 1:
        parts = label.split()
        label = " ".join(parts[:2]) + "\n" + " ".join(parts[2:])
    return label


def plot(
    data: list[Result],
    output_file: str,
    agents: list,
    tasks: dict,
    criteria: dict,
    colors: list[str],
    math_benchmark: bool,
) -> None:
    number_agents = len(agents)
    width = 0.08
    levels = {
        "E": "Easy",
        "M": "Medium",
        "H": "Hard",
    }
    split_index = 2

    if math_benchmark:
        split_index = 1
        found_lvls = sorted(set([tasks[t].split(".")[-split_index] for t in tasks]))
        levels = {}
        for l in found_lvls:
            levels[l] = f"Level {l}"

    x = np.arange(len(levels))
    fig, axs = plt.subplots(len(criteria), sharex=True, sharey=False, figsize=(11, 6))
    handles = []
    for ci, criterion in enumerate(criteria):
        values = []
        for ai, agent in enumerate(agents):
            scores = [
                [
                    float(getattr(d, criterion))
                    for d in data
                    if d.agent == agent and tasks[d.task].split(".")[-split_index] == level
                ]
                for level in levels
            ]
            processed = [
                interquartile_mean(s) #if criterion == "costs" else statistics.mean(s)
                for s in scores
            ]
            number_of_scores = [len(e) for e in scores]
            processed_rounded = [round(e, 4) for e in processed]
            print(f"{criterion} - {agent} - {number_of_scores} - {processed_rounded}")

            bar = axs[ci].bar(
                x - (number_agents - 1) / 2 * width + width * ai,
                processed,
                width,
                color=colors[ai],
                label=agent,
            )
            if ci == 0:  # Only add the legend info from the first subplot
                handles.append(bar)
            values.extend(processed)

        # horizontal lines
        max_value = max(values)
        y_line_positions = [0.25 * max_value, 0.5 * max_value, 0.75 * max_value]
        for y_line_position in y_line_positions:
            axs[ci].axhline(y=y_line_position, color="darkgrey", linestyle="--", linewidth=0.5)

        axs[ci].set_ylabel(criteria[criterion])
        if criterion == "correctness":
            axs[ci].set_ylim(0, 1.0)

        axs[ci].set_axisbelow(True)
        axs[ci].grid(which='major', axis='y', linestyle='--', linewidth=1, alpha=0.5)

        # axs[ci].xaxis.set_major_locator(MultipleLocator(0.2))
        # axs[0].xaxis.set_major_formatter('{x:.0f}')
        # axs[0].xaxis.set_minor_locator(MultipleLocator(minor_grid_x))

        # axs[0].yaxis.set_major_locator(MultipleLocator(major_grid_y))
        # axs[0].yaxis.set_minor_locator(MultipleLocator(minor_grid_y))

    fig.legend(
        handles=[h[0] for h in handles],
        labels=agents,
        loc="upper center",
        ncol=math.ceil(number_agents / 1),
        title="Frameworks",
        borderaxespad=0.2,
    )
    plt.xticks(x, list(levels.values()), rotation=0)
    # plt.ylim(0, 1.0)
    plt.xlabel("Difficulty")


    plt.savefig(output_file, bbox_inches="tight")


def find_most_recent_log(directory: str) -> str:
    pattern = re.compile(r"math\.eval\.(\d{8}-\d{4})\.log")
    files = os.listdir(directory)
    log_files = []
    for file in files:
        match = pattern.match(file)
        if match:
            timestamp_str = match.group(1)
            timestamp = datetime.strptime(timestamp_str, "%Y%m%d-%H%M")
            log_files.append((directory + "/" + file, timestamp))
    if not log_files:
        raise ValueError("No log file found. Run the evaluation first.")
    log_files.sort(key=lambda x: x[1], reverse=True)
    latest_log, latest_timestamp = log_files[0]
    logger.info(f"Using log {latest_log} from {latest_timestamp}.")
    return latest_log


def main(
    log_files: list[str],
    model: str,
    embedding_model: str,
    ground_truths: list[str],
    plot_file: str,
    agents: list,
    criteria: dict,
    colors: list,
    math_benchmark: bool,
) -> None:
    all_results = []
    all_tasks = dict()

    for idx, (log_file, ground_truth) in enumerate(zip(log_files, ground_truths)):
        res = extract_data_from_log(
            log_file=log_file, model=model, embedding_model=embedding_model
        )
        res, tasks = assess_data(results=res, ground_truth=ground_truth)

        all_results.extend(res)
        all_tasks.update(tasks)

        with open(f"./logs/failures_{idx}.txt", "w") as file:
            for r in res:
                if not r.correctness and r.agent == "CotTulipAgent":
                    file.write(f"------ TASK {tasks[r.task]}\n{r.task}\nResponse:\n{r.response}\nGT:{r.ground_truth}\nTools:\n{r.tools_called}\n\n")


    plot(
        data=all_results,
        output_file=plot_file,
        agents=agents,
        tasks=all_tasks,
        criteria=criteria,
        colors=colors,
        math_benchmark=math_benchmark,
    )


def plot_cost_distribution(
    log_file: str,
    ground_truth: str,
    model: str,
    embedding_model: str,
    agents: list[str],
):
    with open(ground_truth, "r") as gtf:
        gtf_data_ = json.load(gtf)
        task_ids = {e["task"]: e["name"] for e in gtf_data_}
    results = extract_data_from_log(
        log_file=log_file, model=model, embedding_model=embedding_model
    )
    sorted_results = {
        "E": {},
        "M": {},
        "H": {},
    }
    for res in results:
        if res.agent not in agents:
            continue
        task_id = task_ids[res.task]
        level = task_id[4]
        if res.agent not in sorted_results[level]:
            sorted_results[level][res.agent] = [res.costs]
        else:
            sorted_results[level][res.agent].append(res.costs)
    dataframes = {
        level: pd.DataFrame(sorted_results[level]) for level in sorted_results.keys()
    }

    fig, axes = plt.subplots(1, len(dataframes), figsize=(14, 6), sharey=True)

    for cdf, level in enumerate(dataframes):
        df = dataframes[level]
        for column in df.columns:
            sns.histplot(
                df[column],
                kde=True,
                label=column,
                stat="density",
                common_norm=False,
                ax=axes[cdf],
            )
        axes[cdf].set_title(level)
        axes[cdf].set_xlabel("Value")
        if cdf == 0:
            axes[cdf].set_ylabel("Density")
        axes[cdf].legend()

    plt.tight_layout()
    plt.show()


def analyze(log_file: str, ground_truth: str, model: str, embedding_model: str) -> None:
    with open(ground_truth, "r") as gtf:
        gtf_data_ = json.load(gtf)
        task_ids = {e["task"]: e["name"] for e in gtf_data_}
    res = extract_data_from_log(
        log_file=log_file, model=model, embedding_model=embedding_model
    )
    res, tasks = assess_data(results=res, ground_truth=ground_truth)
    for r in res:
        if r.agent != "CotTulipAgent":
            continue
        if not r.correctness:
            print(f"INCORRECT: {task_ids[r.task]} - {r.response} - {r.agent}")
        if r.agent != "BaseAgent":
            if r.function_precision < 1:
                print(
                    f"WRONG FUNCTIONS: {task_ids[r.task]} - {r.response} - {r.tools_called}"
                )
            if r.function_recall < 1:
                print(
                    f"MISSING FUNCTIONS: {task_ids[r.task]} - {r.response} - {r.tools_called}"
                )
        print("\n")


def sanity_check_results(
    log_file: str,
    ground_truth: str,
    model: str,
    embedding_model: str,
    agents: list[str],
    runs: int,
) -> bool:
    sane = True
    results = extract_data_from_log(
        log_file=log_file, model=model, embedding_model=embedding_model
    )
    results_sorted = {}
    for r in results:
        if r.task not in results_sorted:
            results_sorted[r.task] = {r.agent: [r]}
        else:
            if r.agent not in results_sorted[r.task]:
                results_sorted[r.task][r.agent] = [r]
            else:
                results_sorted[r.task][r.agent].append(r)
    with open(ground_truth, "r") as gtf:
        gtf_data_ = json.load(gtf)
    for task in gtf_data_:
        if task["task"] not in results_sorted:
            print(f"`{task}`: no results")
            sane = False
            continue
        for agent in agents:
            if agent not in results_sorted[task["task"]]:
                print(f"`{task['task']}` - {agent}: no results")
                sane = False
                continue
            if (number_found := len(results_sorted[task["task"]][agent])) != runs:
                print(f"`{task['task']}` - {agent}: only [{number_found}/{runs}]")
                sane = False
    return sane


if __name__ == "__main__":

    MATH_benchmark = True

    logs_to_plot = [
        "logs/math.eval.20240701-1154.log",
        "logs/math.eval.20240701-1507.log",
    ]
    logs_to_plot = None

    with open("math_eval_settings.yaml", "rt") as mes:
        settings = yaml.safe_load(mes.read())
    log_folder = settings["log_folder"]
    if not logs_to_plot:
        logs_to_plot = [(
            log_folder + "/" + settings["log_file"]
            if settings["log_file"]
            else find_most_recent_log(directory=log_folder)
        )]

    ground_truths = []
    log_names = []
    log_folder = "logs"
    with open(log_folder + "/history.json", "r") as f:
        history_data = json.load(f)
        for log in logs_to_plot:
            log_name = log.split("/")[-1]
            log_names.append(log_name)
            ground_truths.append(history_data[log_name]["ground_truth"])
            model = history_data[log_name]["model"]
            embedding_model = history_data[log_name]["embedding_model"]
            agents = [
                a
                for a in history_data[log_name]["agents"]
                if history_data[log_name]["agents"][a]
            ]
            colors = [history_data[log_name]["colors"][a] for a in agents]

    criteria = {
            "costs": "Costs [$]",
            "function_recall": "Recall",
            "function_precision": "Precision",
            "correctness": "Correct",
        }
    if MATH_benchmark:
        criteria = {
            "costs": "Costs [$]",
            "correctness": "Correct",
        }
    # passed = sanity_check_results(
    #     log_file=log,
    #     model=model,
    #     embedding_model=embedding_model,
    #     ground_truth=history_data[log_name]["ground_truth"],
    #     agents=agents,
    #     runs=history_data[log_name]["number_of_runs"],
    # )
    # if passed is False:
    #     raise ValueError("Sanity check failed - number of results does not match tasks")
    # plot_cost_distribution(
    #     log_file=log,
    #     model=model,
    #     embedding_model=embedding_model,
    #     ground_truth=history_data[log_name]["ground_truth"],
    #     agents=agents,
    # )
    main(
        log_files=logs_to_plot,
        model=model,
        embedding_model=embedding_model,
        ground_truths=ground_truths,
        plot_file="math.eval.png",
        agents=agents,
        criteria=criteria,
        colors=colors,
        math_benchmark=MATH_benchmark,
    )
    if MATH_benchmark:
        img_name = "_".join(ln[:-3] for ln in log_names) + "_math_bench.png"
    else:
        img_name = log_name[:-3] + ".png"
    shutil.copy("math.eval.png", f"{log_folder}/{img_name}")
