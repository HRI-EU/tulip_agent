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
from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import networkx as nx


class Task:
    def __init__(
        self,
        description: str,
        predecessor: Optional[Task] = None,
        successor: Optional[Task] = None,
        supertask: Optional[Task] = None,
        original_wording: Optional[Task] = None,
    ) -> None:
        self.description = description
        self.predecessor: Optional[Task] = predecessor
        self.successor: Optional[Task] = successor
        self.supertask: Optional[Task] = supertask
        self.subtasks: list[Task] = []
        self.tool_candidates: list[Tool] = []
        self.paraphrased_variants: list[Task] = []
        self.original_wording: Optional[Task] = original_wording
        self.result: Optional[str] = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object {id(self)}: {self.description}>"

    def get_predecessors(self) -> list[Task]:
        predecessors = []
        node = self
        while True:
            if not node.predecessor:
                break
            predecessors.append(node.predecessor)
            node = node.predecessor
        return predecessors

    def _get_nodes_and_edges(self, task: Task) -> tuple:
        nodes = [(task, {"node_type": "task"})]
        nodes.extend([(tool, {"node_type": "tool"}) for tool in task.tool_candidates])
        edges = [[task, subtask, {"edge_type": "subtask"}] for subtask in task.subtasks]
        edges.extend(
            [[task, tool, {"edge_type": "tool"}] for tool in task.tool_candidates]
        )
        if task.predecessor:
            edges.append([task.predecessor, task, {"edge_type": "successor"}])
        for subtask in task.subtasks:
            sn, se = self._get_nodes_and_edges(subtask)
            nodes.extend(sn)
            edges.extend(se)
        return nodes, edges

    def plot(self):
        graph = nx.DiGraph()
        nodes, edges = self._get_nodes_and_edges(self)
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)
        pos = nx.spiral_layout(graph)
        plt.figure(figsize=(16, 12))

        # Nodes and edges by types
        task_nodes = [n for n, d in graph.nodes(data=True) if d["node_type"] == "task"]
        tool_nodes = [n for n, d in graph.nodes(data=True) if d["node_type"] == "tool"]
        subtask_edges = [
            (u, v) for u, v, d in graph.edges(data=True) if d["edge_type"] == "subtask"
        ]
        successor_edges = [
            (u, v)
            for u, v, d in graph.edges(data=True)
            if d["edge_type"] == "successor"
        ]
        tool_edges = [
            (u, v) for u, v, d in graph.edges(data=True) if d["edge_type"] == "tool"
        ]

        # Draw
        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=task_nodes,
            node_shape="o",
            node_color="lightblue",
            node_size=500,
        )
        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=tool_nodes,
            node_shape="o",
            node_color="lightgrey",
            node_size=500,
        )
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=subtask_edges,
            arrowstyle="->",
            arrowsize=20,
            edge_color="black",
        )
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=successor_edges,
            arrowstyle="->",
            arrowsize=20,
            style="dashed",
            edge_color="grey",
        )
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=tool_edges,
            arrowstyle="->",
            arrowsize=20,
            style="dotted",
            edge_color="grey",
        )
        nx.draw_networkx_labels(graph, pos, font_size=10)
        plt.show()


class Tool:
    def __init__(
        self,
        name: str,
        description: dict,
    ) -> None:
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object {id(self)}: {self.name}>"


if __name__ == "__main__":
    # example
    q = "mix a margherita, prepare a pineapple pizza, and turn on the radiator"
    t0 = Task(description=q)
    print(t0.__dict__)
    # eg, no tools found, decompose further
    subtask_descriptions = [
        "mix a margherita",
        "prepare a pineapple pizza",
        "turn on the radiator",
    ]
    subtasks = [Task(description=d, supertask=t0) for d in subtask_descriptions]
    for s1, s2 in zip(subtasks, subtasks[1:]):
        s1.successor = s2
        s2.predecessor = s1
    for s in subtasks:
        s.tool_candidates = [Tool(name=f"{s.description} tool", description={})]
    t0.subtasks = subtasks
    for st in subtasks:
        print(st.__dict__)
    print(t0.__dict__)
    t0.plot()
