#!/usr/bin/env python3
import ast
import json
import logging.config
import matplotlib.pyplot as plt
import numpy as np
import yaml

from collections import Counter
from dataclasses import dataclass
from typing import Optional


# Set up logger
with open("logging_config.yaml", "rt") as log_config:
    config = yaml.safe_load(log_config.read())
logging.config.dictConfig(config)
logger = logging.getLogger("result_analysis")


# source: https://openai.com/pricing, all in cents
OAI_PRICES = {
    "gpt_4_input": 10 / 1_000_000,
    "gpt_4_output": 30 / 1_000_000,
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
                OAI_PRICES["gpt_4_input"] * self.input_tokens
                + OAI_PRICES["gpt_4_output"] * self.completion_tokens
                + OAI_PRICES["ada_embed"] * self.embedding_tokens
            ),
            2,
        )


def extract_data_from_log(log_file: str) -> list[Result]:
    results = []
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
                tool_name = log_line.split(" - INFO - Function ")[-1].split()[0]
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
        r = Result(
            agent=agent,
            task=query,
            input_tokens=in_tokens,
            completion_tokens=out_tokens,
            embedding_tokens=embed_tokens,
            tools_called=tools_called,
            response=response,
        )
        results.append(r)
        logger.info(f"Retrieved data for {r.agent} on `{r.task}`.")
    return results


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
) -> None:
    number_agents = len(agents)
    width = 0.05
    color_dict = {
        "dark grey": "#999999",
        "lighter blue": "#98c6ea",
        "dark blue": "#005293",
        "light grey": "#dad7cb",
        "light blue": "#64a0c8",
        "tum blue": "#0065bd",
        "orange": "#e37222",
        "green": "#a2ad00",
    }
    colors = list(color_dict.values())
    x = np.arange(len(tasks))
    fig, axs = plt.subplots(len(criteria), sharex=True, sharey=False, figsize=(10, 5))
    for ci, criterion in enumerate(criteria):
        for ai, agent in enumerate(agents):
            _ = axs[ci].bar(
                x - (number_agents - 1) / 2 * width + width * ai,
                [
                    float(getattr(d, criterion))
                    for task in tasks
                    for d in data
                    if d.agent == agent and d.task == task
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
    plt.xticks(x, list(tasks.values()), rotation=0)
    # plt.ylim(0, 1.0)
    plt.xlabel("Tasks")
    plt.savefig(output_file, bbox_inches="tight")


def main(
    log_file: str, ground_truth: str, plot_file: str, agents: list, criteria: dict
) -> None:
    res = extract_data_from_log(log_file=log_file)
    res, tasks = assess_data(results=res, ground_truth=ground_truth)
    for r in res:
        print(r)
    plot(data=res, output_file=plot_file, agents=agents, tasks=tasks, criteria=criteria)


if __name__ == "__main__":
    main(
        log_file="math.eval.2.log",
        ground_truth="math_tasks.json",
        plot_file="math.eval.png",
        agents=[
            "BaseAgent",
            "ToolAgent",
            "ToolCotAgent",
            "MinimalTulipAgent",
            "NaiveTulipAgent",
            "TulipCotAgent",
            "AutoTulipAgent",
        ],
        criteria={
            "costs": "Costs [$]",
            "function_recall": "Recall",
            "function_precision": "Precision",
            "correctness": "Correct",
        },
    )
