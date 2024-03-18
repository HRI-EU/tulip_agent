# 🌷🤖 tulip agent
A reference implementation for the `tulip agent`, an LLM-backed agent with access to a large number of tools via a tool library. \
This approach is helpful whenever the number of tools available exceeds the LLM's context window or would
otherwise lead to challenges for the LLM to find the right tool for the task.

## Contents
* `function_analyzer`: Python function introspection for generating tool descriptions
* `tool_library`: Vector store for managing tools
* `tulip_agent`: Agent with tool access - several variants

## Dev notes
* Python v3.10.11 recommended, higher versions may lead to issues with chroma when installing via Poetry
* [Pre-commit hooks](https://pre-commit.com/) - install with `(poetry run) pre-commit install`
* Linting: [ruff](https://github.com/astral-sh/ruff)
* Formatting: [black](https://github.com/psf/black)
