#!/usr/bin/env python3
import logging

from tulip_agent import AutoTulipAgent, ToolLibrary


# Set logger to INFO to show agents' internal steps
logging.basicConfig(level=logging.INFO)

task = """What is the square root of 23456789?"""

tulip = ToolLibrary(chroma_sub_dir="auto/")
ata = AutoTulipAgent(tool_library=tulip, top_k_functions=3)

res = ata.query(prompt=task)

print(f"{task=}")
print(f"{res=}")
