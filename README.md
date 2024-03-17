# 🌷 tulip agent
A reference implementation for an LLM-backed agent using vector retrieval for accessing large tool libraries. \
This approach is helpful whenever the number of tools available exceeds the LLM's context window or would 
otherwise lead to challenges for the LLM to find the correct one.

## Contents
* `tulip_agent`: agent with tool access - several variants
* `tool_library`: vector store for managing tools

## Dev notes
* Python v3.10.11 recommended, higher versions may lead to issues with chroma when installing via Poetry
* Linting: ruff
* Formatting: black
