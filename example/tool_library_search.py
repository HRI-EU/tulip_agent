#!/usr/bin/env python3
import logging

from tulip_agent import ToolLibrary


# Set logger to INFO to show agents' internal steps
logging.basicConfig(level=logging.INFO)

tasks = [
    """Add 2 and 5""",
    """Calculate the product of 2 and 5.""",
    """Calculate the square root of 8.""",
    """What is 2 + 5?""",
    """What is 2 + 4 / 3?""",
    """Draw a horse""",
]

tulip = ToolLibrary(chroma_sub_dir="example/", file_imports=[("calculator", [])])

for task in tasks:
    print(f"{task=}")
    res = tulip.search(problem_description=task, top_k=4, similarity_threshold=0.35)
    print(f"{res=}")
