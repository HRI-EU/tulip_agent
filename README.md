# 🌷🤖 tulip agent

![tulip banner](docs/static/images/tulip-banner.png)

[![Static Badge](https://img.shields.io/badge/arXiv-2407.21778-B31B1B?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2407.21778)
[![License](https://img.shields.io/pypi/l/cobras?style=flat-square)](https://opensource.org/license/bsd-3-clause)
[![Code Style](https://img.shields.io/badge/code_style-black-black?style=flat-square)](https://github.com/psf/black)

A reference implementation for the `tulip agent`, an LLM-backed agent with access to a large number of tools via a tool library.
This approach reduces costs, enables the use of tool sets that exceed API limits or context windows, and increases flexibility with regard to the tool set used.

## Key components
🔬 **Function analysis** \
Generate OpenAI API compatible tool descriptions for Python functions via introspection

🌷 **Tool library** \
Combines a vector store for semantic search among tools and tool execution

🤖 **Agents**
* Baseline, without tool library
  * `BaseAgent`: LLM agent without tool access
  * `NaiveToolAgent`: Includes tool descriptions for all tools available
  * `CotToolAgent`: Extends the `NaiveToolAgent` with a planning step that decomposes the user input into subtasks
* Tulip variations with access to a tool library
  * `MinimalTulipAgent`: Minimal implementation; searches for tools based on the user input directly
  * `NaiveTulipAgent`: Naive implementation; searches for tools with a separate tool call
  * `CotTulipAgent`: COT implementation; derives a plan for the necessary steps and searches for suitable tools
  * `InformedCotTulipAgent`: Same as `CotTulipAgent`, but with a brief description of the tool library's contents
  * `PrimedCotTulipAgent`: Same as `CotTulipAgent`, but primed with tool names based on an initial search with the user request
  * `OneShotCotTulipAgent`: Same as `CotTulipAgent`, but the system prompt included a brief example
  * `AutoTulipAgent`: Fully autonomous variant; can use the search tool at any time and modify its tool library with CRUD operations
  * `DfsTulipAgent`: DFS inspired variant that leverages a DAG for keeping track of tasks and suitable tools, can create new tools

📊 **Evaluation**
* `math_eval`: Math evaluation
* `robo_eval`: Robotics evaluation using tools created for [AttentiveSupport](https://github.com/HRI-EU/AttentiveSupport)

📝 **Examples** \
See `./examples`


## Setup
* Make sure you have an OpenAI API key set up, see the [official instructions](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)
* Install with `poetry install` or `pip install -e .`
* Check out the `examples` and the robot evaluation in `src/robo_eval`


## Dev notes
* Python v3.10.11 recommended, higher versions may lead to issues with chroma when installing via Poetry
* [Pre-commit hooks](https://pre-commit.com/) - install with `(poetry run) pre-commit install`
* Linting: [ruff](https://github.com/astral-sh/ruff)
* Formatting: [black](https://github.com/psf/black)
* Import sorting: [isort](https://github.com/PyCQA/isort)
* Tests: Run with `(poetry run) python -m unittest discover tests/`


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

### Running the example results in a ModuleNotFoundError
Make sure to install the package itself, e.g., with `poetry install` or `pip install -e .` \
Then run the example with `poetry run python examples/calculator_example.py`
