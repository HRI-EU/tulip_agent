#!/usr/bin/env python3
import logging
import os

from tulip_agent import AutoTulipAgent, ToolLibrary


# Set logger to INFO to show agents' internal steps
logging.basicConfig(level=logging.INFO)

tasks = [
    """What is the square root of 23456789?""",
    """Delete the square root function.""",
]

tulip = ToolLibrary(chroma_sub_dir="auto/")
ata = AutoTulipAgent(tool_library=tulip, top_k_functions=3)

for task in tasks:
    print(f"{task=}")
    res = ata.query(prompt=task)
    print(f"{res=}")

# cleanup
for m in {e["module_name"] for e in tulip.function_origins.values()}:
    os.remove(m + ".py")
