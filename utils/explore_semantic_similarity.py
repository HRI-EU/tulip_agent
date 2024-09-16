#!/usr/bin/env python3
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

from tulip_agent.embed import embed


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

emb_tool = np.array(embed(tool))
for task in tasks:
    print(f"Task: {task}")
    emb_task = np.array(embed(task))
    l2squared = np.linalg.norm(emb_task - emb_tool)
    print(f"L2squared distance: {l2squared}")
    cosine_dist = 1 - np.dot(emb_task, emb_tool) / (
        np.linalg.norm(emb_task) * np.linalg.norm(emb_tool)
    )
    print(f"Cosine similarity distance: {cosine_dist}")
    print()
