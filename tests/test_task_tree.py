#!/usr/bin/env python3
#
#  Copyright (c) 2024-2025, Honda Research Institute Europe GmbH
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  SPDX-License-Identifier: BSD-3-Clause
#
#
import pytest

from tulip_agent.task import Task
from tulip_agent.tool import ImportedTool


def test_get_predecessors_without_higher(task_tree):
    _, st2c = task_tree

    predecessors = st2c.get_predecessors(include_higher_levels=False)

    assert [p.description for p in predecessors] == ["t2b", "t2a"]


def test_get_predecessors_with_higher(task_tree):
    _, st2c = task_tree

    predecessors = st2c.get_predecessors(include_higher_levels=True)

    assert [p.description for p in predecessors] == ["t2b", "t2a", "t1"]


def test_get_nodes_and_edges(task_tree):
    task, _ = task_tree

    nodes, edges = task._get_nodes_and_edges(task)

    assert len(nodes) == 14  # 7 tasks, 7 tools
    assert len(edges) == 17  # 6 subtask, 7 tool, 4 predecessor edges


def _add_subtasks(task: Task, subtask_names: list[str]):
    subtasks = [Task(description=d, supertask=task) for d in subtask_names]
    for s1, s2 in zip(subtasks, subtasks[1:]):
        s1.successor = s2
        s2.predecessor = s1
    for s in subtasks:
        s.tool_candidates = [
            ImportedTool(
                function_name=f"{s.description}_tool",
                module_name="tests.example_tools_for_tree",
                definition={"function": {"description": "dummy"}},
            )
        ]
    task.subtasks.append(subtasks)


def _tool_for_task(task: Task) -> ImportedTool:
    return ImportedTool(
        function_name=f"{task.description}_tool",
        module_name="tests.example_tools_for_tree",
        definition={"function": {"description": "dummy"}},
    )


@pytest.fixture
def task_tree():
    task = Task(description="t")
    task.tool_candidates = [_tool_for_task(task)]
    _add_subtasks(task, subtask_names=["t1", "t2", "t3"])
    st2 = task.subtasks[-1][1]
    _add_subtasks(task=st2, subtask_names=["t2a", "t2b", "t2c"])
    return task, st2.subtasks[-1][2]
