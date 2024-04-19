#!/usr/bin/env python3
import logging

from tulip_agent import TulipCotAgent, ToolLibrary


# Set logger to INFO to show agents' internal steps
logging.basicConfig(level=logging.INFO)

tasks = ["""Add 2 and 5""", """Add the product of 3 and 4 and the product of 5 and 6"""]

tulip = ToolLibrary(chroma_sub_dir="example/", file_imports=[("calculator", [])])
ata = TulipCotAgent(tool_library=tulip, top_k_functions=3)

for task in tasks:
    print(f"{task=}")
    res = ata.query(prompt=task)
    print(f"{res=}")
