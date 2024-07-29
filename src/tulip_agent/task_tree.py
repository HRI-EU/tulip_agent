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


class Task:
    def __init__(
        self,
        description: str,
        predecessor: Optional[Task] = None,
        successor: Optional[Task] = None,
    ) -> None:
        self.description = description
        self.predecessor: Optional[Task] = predecessor
        self.successor: Optional[Task] = successor
        self.subtasks: Optional[list[Task]] = None
        self.tool_candidates: Optional[list[dict]] = None
        self.paraphrased_descriptions: list[str] = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object {id(self)}: {self.description}>"


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
    subtasks = [Task(description=d) for d in subtask_descriptions]
    for s1, s2 in zip(subtasks, subtasks[1:]):
        s1.successor = s2
        s2.predecessor = s1
    t0.subtasks = subtasks
    for st in subtasks:
        print(st.__dict__)
    print(t0.__dict__)
