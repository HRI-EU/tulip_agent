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
import numpy as np
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
    "ada_embed": 0.1 / 1_000_000,
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
    input_tokens: int
    completion_tokens: int
    embedding_tokens: int
    tools_called: list[ToolCall]
    response: str
    costs: Optional[float] = None
    function_precision: Optional[float] = None
    function_recall: Optional[float] = None
    correctness: Optional[bool] = None

    def __post_init__(self) -> None:
        self.costs = round(
            (
                OAI_PRICES[self.model]["input"] * self.input_tokens
                + OAI_PRICES[self.model]["output"] * self.completion_tokens
                + OAI_PRICES["ada_embed"] * self.embedding_tokens
            ),
            2,
        )


def extract_data_from_log(log_file: str, model: str) -> list[Result]:
    results = []
    tool_library_costs = calc_costs_for_tool_library()
    with open(log_file, "r") as f:
        logs = f.read()
    parts, current = [], []
    for line in logs.strip().split("\n2024-"):
        current.append(line)
        if "returns response" in line:
            parts.append(current)
            current = []
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
                tool_arguments = ast.literal_eval(
                    log_line.split(" for arguments ")[-1][:-1]
                )
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
            input_tokens=in_tokens,
            completion_tokens=out_tokens,
            embedding_tokens=embed_tokens,
            tools_called=tools_called,
            response=response,
        )
        results.append(r)
        logger.info(f"Retrieved data for {r.agent} on `{r.task}`.")
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
        logger.info(f"Assessing {r.agent} on `{r.task}`.")
        if r.task not in gtf_data:
            logger.warning(f"No ground truth found for {r.task}")
            continue
        r.correctness = any(
            str(vs) in r.response for vs in gtf_data[r.task]["valid_solutions"]
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
        r.function_recall = len(relevant_tools) / len(gtf_data[r.task]["functions"])
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
) -> None:
    number_agents = len(agents)
    width = 0.05
    levels = {
        "E": "Easy",
        "M": "Medium",
        "H": "Hard",
    }
    x = np.arange(len(levels))
    fig, axs = plt.subplots(len(criteria), sharex=True, sharey=False, figsize=(10, 5))
    for ci, criterion in enumerate(criteria):
        for ai, agent in enumerate(agents):
            _ = axs[ci].bar(
                x - (number_agents - 1) / 2 * width + width * ai,
                [
                    statistics.mean(
                        [
                            float(getattr(d, criterion))
                            for d in data
                            if d.agent == agent
                            and tasks[d.task].split(".")[-2] == level
                        ]
                    )
                    for level in levels
                ],
                width,
                color=colors[ai],
                label=agent,
            )
        axs[ci].set_ylabel(criteria[criterion])
    fig.legend(
        axs[0].get_children(),
        labels=agents,
        loc="upper center",
        ncol=number_agents,
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
    log_file: str,
    model: str,
    ground_truth: str,
    plot_file: str,
    agents: list,
    criteria: dict,
    colors: list,
) -> None:
    res = extract_data_from_log(log_file=log_file, model=model)
    res, tasks = assess_data(results=res, ground_truth=ground_truth)
    for r in res:
        print(r)
    plot(
        data=res,
        output_file=plot_file,
        agents=agents,
        tasks=tasks,
        criteria=criteria,
        colors=colors,
    )


def analyze(log_file: str, ground_truth: str) -> None:
    with open(ground_truth, "r") as gtf:
        gtf_data_ = json.load(gtf)
        task_ids = {e["task"]: e["name"] for e in gtf_data_}
    res = extract_data_from_log(log_file=log_file)
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


if __name__ == "__main__":
    with open("math_eval_settings.yaml", "rt") as mes:
        settings = yaml.safe_load(mes.read())
    log_folder = settings["log_folder"]
    log = (
        log_folder + "/" + settings["log_file"]
        if settings["log_file"]
        else find_most_recent_log(directory=log_folder)
    )
    with open(log_folder + "/history.json", "r") as f:
        history_data = json.load(f)
        log_name = log.split("/")[-1]
        model = history_data[log_name]["model"]
        agents = [
            a
            for a in history_data[log_name]["agents"]
            if history_data[log_name]["agents"][a]
        ]
        colors = [history_data[log_name]["colors"][a] for a in agents]
    main(
        log_file=log,
        model=model,
        ground_truth=settings["ground_truth"],
        plot_file="math.eval.png",
        agents=agents,
        criteria={
            "costs": "Costs [$]",
            "function_recall": "Recall",
            "function_precision": "Precision",
            "correctness": "Correct",
        },
        colors=colors,
    )
    img_name = log_name[:-3] + "png"
    shutil.copy("math.eval.png", f"{log_folder}/{img_name}")
