# 🌷🤖 tulip agent
A reference implementation for the `tulip agent`, an LLM-backed agent with access to a large number of tools via a tool library. \
This approach is helpful whenever the number of tools available exceeds the LLM's context window or would
otherwise lead to challenges for the LLM to find the right tool for the task.

## Contents
* `function_analyzer`: Python function introspection for generating tool descriptions
* `tool_library`: Vector store for managing tools
* `tulip_agent`: Agents with tool access
  * `MinimalTulipAgent`: Minimal implementation; searches for tools based on user input directly
  * `NaiveTulipAgent`: Naive implementation; searches for tools with a separate tool call
  * `TulipCotAgent`: COT implementation; derives a plan for the necessary steps and searches for dedicated tools
  * `AutoTulipAgent`: Fully autonomous variant; may use the search tool at any time
* `base_agent`: Conventional baseline
  * `BaseAgent`: Uses regular tool descriptions in its system prompt


## Dev notes
* Python v3.10.11 recommended, higher versions may lead to issues with chroma when installing via Poetry
* [Pre-commit hooks](https://pre-commit.com/) - install with `(poetry run) pre-commit install`
* Linting: [ruff](https://github.com/astral-sh/ruff)
* Formatting: [black](https://github.com/psf/black)


## Known issues

### SQLite version incompatibility
See these [troubleshooting instructions](https://docs.trychroma.com/troubleshooting#sqlite)
1. On Linux install pysqlite3-binary: `poetry add pysqlite3-binary`
2. Add the following to `lib/python3.10/site-packages/chromadb/__init__.py` in your venv
```python
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
```
