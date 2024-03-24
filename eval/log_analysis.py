#!/usr/bin/env python3
import ast

from dataclasses import dataclass


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


class Analyzer:

    @staticmethod
    def analyze_log(log_file: str) -> list[Result]:
        results = []
        with open(log_file, "r") as f:
            logs = f.read()
        parts, current = [], []
        for line in logs.strip().split("\n"):
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
                    token_counts = log_line.split(" in tokens: ")[-1].split(
                        " completion."
                    )[0]
                    i, o = token_counts.split(" prompt and ")
                    in_tokens += int(i)
                    out_tokens += int(o)
                elif "Usage for embedding in tokens" in log_line:
                    embed_tokens += int(
                        log_line.split("Usage for embedding in tokens: ")[-1].split(
                            " prompt."
                        )[0]
                    )
                elif all(
                    w in log_line for w in ("Function", "returned", "for arguments")
                ):
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
            results.append(
                Result(
                    agent=agent,
                    task=query,
                    input_tokens=in_tokens,
                    completion_tokens=out_tokens,
                    embedding_tokens=embed_tokens,
                    tools_called=tools_called,
                    response=response,
                )
            )
        return results


if __name__ == "__main__":
    analyzer = Analyzer()
    res = analyzer.analyze_log("math.eval.log")
    for r in res:
        print(r)
