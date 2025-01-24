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
"""
Utility for exploring semantic similarity thresholds; which may depend on the application.

Note: OpenAI recommends cosine similarity, but embeddings are normalized, so the rankings
for cosine similarity and euclidian are identical
https://help.openai.com/en/articles/6824809-embeddings-frequently-asked-questions

Insight:
1.25 seems to be a reasonable cutoff for l2-squared
this still includes aggregate functions but not completely unrelated ones
"""

import numpy as np
from openai import OpenAI

from tulip_agent.embed import embed


client = OpenAI()

embedding_models = (
    "text-embedding-ada-002",
    "text-embedding-3-small",
    "text-embedding-3-large",
)
embedding_model = embedding_models[0]

tasks = [
    "Prepare the car for the trip.",
    "This sentence should be completely different because it is about horses.",
    "Take a photo and convert it to jpg.",
    "Calculate the square root of the sum of the product of 3 and 4 and the product of 5 and 6",
    "Add the contents of the two milk containers.",
    "Return the sum of 1 and 2.",
    "Add two numbers and subtract a third number.",
    "Add two numbers.",
]
tool = "add:\nAdds two numbers together."

emb_tool = np.array(embed(tool, client))
for task in tasks:
    print(f"Task: {task}")
    emb_task = np.array(embed(task, client))
    l2squared = np.linalg.norm(emb_task - emb_tool)
    print(f"L2squared distance: {l2squared}")
    cosine_dist = 1 - np.dot(emb_task, emb_tool) / (
        np.linalg.norm(emb_task) * np.linalg.norm(emb_tool)
    )
    print(f"Cosine similarity distance: {cosine_dist}")
    print()
