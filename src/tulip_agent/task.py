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

from dataclasses import dataclass, field
from typing import Optional

import matplotlib.pyplot as plt
import networkx as nx

from tulip_agent.tool import Tool


@dataclass(eq=False)
class Task:
    description: str
    predecessor: Optional[Task] = None
    successor: Optional[Task] = None
    supertask: Optional[Task] = None

    subtasks: list[list[Task]] = field(default_factory=list, init=False)
    tool_candidates: list[Tool] = field(default_factory=list, init=False)
    paraphrased_variants: list[Task] = field(default_factory=list, init=False)
    generated_tools: list[Tool] = field(default_factory=list, init=False)
    result: Optional[str] = field(default=None, init=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object {id(self)}: {self.description}>"

    def validate(self) -> bool:
        if self.subtasks:
            results = []
            for subtask in self.subtasks[-1]:
                result_ = subtask.validate()
                results.append(result_)
            valid = all(results)
        else:
            assert (
                lntc := len(self.tool_candidates)
            ) == 1, f"Number of tool candidates is {lntc} instead of 1 for {self.description}."
            if self.tool_candidates[0].predecessor:
                valid = (
                    self.tool_candidates[0].predecessor
                    == self.predecessor.tool_candidates[0].unique_id
                )
                if valid is False:
                    print(self.description)
            else:
                valid = True
        return valid

    def get_predecessors(
        self,
        include_higher_levels: bool = True,
    ) -> list[Task]:
        predecessors = []
        node = self
        while True:
            if not node.predecessor:
                if include_higher_levels and node.supertask:
                    node = node.supertask
                    continue
                break
            predecessors.append(node.predecessor)
            node = node.predecessor
        return predecessors

    def _get_nodes_and_edges(self, task: Task) -> tuple:
        nodes = [(task, {"node_type": "task"})]
        nodes.extend([(tool, {"node_type": "tool"}) for tool in task.tool_candidates])
        edges = [
            [task, subtask, {"edge_type": "subtask"}]
            for subtask_list in task.subtasks
            for subtask in subtask_list
        ]
        edges.extend(
            [[task, tool, {"edge_type": "tool"}] for tool in task.tool_candidates]
        )
        if task.paraphrased_variants:
            nodes.append((task.paraphrased_variants[-1], {"node_type": "task"}))
            edges.append(
                [task, task.paraphrased_variants[-1], {"edge_type": "paraphrased"}]
            )
            sn, se = self._get_nodes_and_edges(task.paraphrased_variants[-1])
            nodes.extend(sn)
            edges.extend(se)
        if task.successor:
            edges.append([task, task.successor, {"edge_type": "successor"}])
        if task.generated_tools:
            nodes.extend(
                [(tool, {"node_type": "tool"}) for tool in task.generated_tools]
            )
            edges.extend(
                [
                    [task, tool, {"edge_type": "generated_tool"}]
                    for tool in task.generated_tools
                ]
            )
        for subtask_list in task.subtasks:
            for subtask in subtask_list:
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
        paraphrased_nodes = [
            n for n, d in graph.nodes(data=True) if d["node_type"] == "paraphrased_task"
        ]
        tool_nodes = [n for n, d in graph.nodes(data=True) if d["node_type"] == "tool"]
        subtask_edges = [
            (u, v) for u, v, d in graph.edges(data=True) if d["edge_type"] == "subtask"
        ]
        successor_edges = [
            (u, v)
            for u, v, d in graph.edges(data=True)
            if d["edge_type"] == "successor"
        ]
        paraphrased_edges = [
            (u, v)
            for u, v, d in graph.edges(data=True)
            if d["edge_type"] == "paraphrased"
        ]
        tool_edges = [
            (u, v) for u, v, d in graph.edges(data=True) if d["edge_type"] == "tool"
        ]
        generated_tool_edges = [
            (u, v)
            for u, v, d in graph.edges(data=True)
            if d["edge_type"] == "generated_tool"
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
            nodelist=paraphrased_nodes,
            node_shape="o",
            node_color="lightsalmon",
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
            edgelist=paraphrased_edges,
            arrowstyle="->",
            arrowsize=20,
            style="dotted",
            edge_color="salmon",
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
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=generated_tool_edges,
            arrowstyle="->",
            arrowsize=20,
            style="dotted",
            edge_color="blue",
        )
        nx.draw_networkx_labels(graph, pos, font_size=10)
        plt.show()
