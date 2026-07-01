#!/usr/bin/env python3
#
#  Copyright (c) 2024-2025, Honda Research Institute Europe GmbH
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  SPDX-License-Identifier: BSD-3-Clause
#
#
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from tests import example_tools
from tests.example_tools_in_class import Calculator
from tulip_agent.tool import McpTool
from tulip_agent.tool_execution import Job, execute_parallel_jobs
from tulip_agent.tool_library import ToolLibrary


def test_init(tool_library_factory):
    tulip = tool_library_factory(file_imports=[("tests.example_tools", [])])

    assert _ids(tulip) == {"add", "subtract", "multiply", "divide", "slow", "speak"}


def test_init_verbose_id(tool_library_factory):
    tulip = tool_library_factory(
        file_imports=[("tests.example_tools", [])],
        verbose_tool_ids=True,
    )

    assert _ids(tulip) == {
        "tests__example_tools__add",
        "tests__example_tools__subtract",
        "tests__example_tools__multiply",
        "tests__example_tools__divide",
        "tests__example_tools__slow",
        "tests__example_tools__speak",
    }


def test_init_specific(tool_library_factory):
    tulip = tool_library_factory(file_imports=[("tests.example_tools", ["add"])])

    assert _ids(tulip) == {"add"}


def test_init_functions(tool_library_factory):
    tulip = tool_library_factory(
        function_imports=[example_tools.add, example_tools.subtract],
    )

    assert _ids(tulip) == {"add", "subtract"}


def test_init_functions_unspecified(tool_library_factory):
    first = tool_library_factory(
        chroma_sub_dir="reused/",
        function_imports=[example_tools.add, example_tools.subtract],
    )
    assert _ids(first) == {"add", "subtract"}

    second = tool_library_factory(
        chroma_sub_dir="reused/",
        function_imports=[example_tools.add],
    )

    assert _ids(second) == {"add"}


def test_init_instance(tool_library_factory):
    calculator = Calculator(divisor=3)

    tulip = tool_library_factory(instance_imports=[calculator])

    assert _ids(tulip) == {"add", "custom_division"}


def test_init_instance_verbose_id(tool_library_factory):
    calculator = Calculator(divisor=3)

    tulip = tool_library_factory(
        instance_imports=[calculator],
        verbose_tool_ids=True,
    )

    assert _ids(tulip) == {
        "tests__example_tools_in_class__Calculator__add",
        "tests__example_tools_in_class__Calculator__custom_division",
    }


def test_init_file_unspecified(tool_library_factory):
    first = tool_library_factory(
        chroma_sub_dir="reused/",
        file_imports=[("tests.example_tools", [])],
    )
    assert len(_ids(first)) == 6

    second = tool_library_factory(chroma_sub_dir="reused/")

    assert len(_ids(second)) == 0


def test_init_specific_unspecified(tool_library_factory):
    first = tool_library_factory(
        chroma_sub_dir="reused/",
        file_imports=[("tests.example_tools", ["add", "subtract"])],
    )
    assert _ids(first) == {"add", "subtract"}

    second = tool_library_factory(
        chroma_sub_dir="reused/",
        file_imports=[("tests.example_tools", ["add"])],
    )

    assert _ids(second) == {"add"}


def test_init_instance_unspecified(tool_library_factory):
    calculator = Calculator(divisor=3)
    first = tool_library_factory(
        chroma_sub_dir="reused/",
        instance_imports=[calculator],
    )
    assert len(_ids(first)) == 2

    second = tool_library_factory(chroma_sub_dir="reused/")

    assert len(_ids(second)) == 0


def test_init_name_clash(tool_library_factory):
    calculator = Calculator(divisor=3)

    with pytest.raises(ValueError):
        tool_library_factory(
            file_imports=[("tests.example_tools", ["add"])],
            instance_imports=[calculator],
        )


def test_duplicate_instances_rejected(tool_library_factory):
    with pytest.raises(ValueError, match="Duplicate instances"):
        tool_library_factory(
            instance_imports=[Calculator(divisor=3), Calculator(divisor=4)]
        )


def test_init_no_name_clash(tool_library_factory):
    calculator = Calculator(divisor=3)

    tulip = tool_library_factory(
        file_imports=[("tests.example_tools", ["add"])],
        instance_imports=[calculator],
        verbose_tool_ids=True,
    )

    assert _ids(tulip) == {
        "tests__example_tools__add",
        "tests__example_tools_in_class__Calculator__add",
        "tests__example_tools_in_class__Calculator__custom_division",
    }


def test_load_file(tool_library_factory):
    tulip = tool_library_factory()

    tulip.load_functions_from_file(
        module_name="tests.example_tools",
        function_names=[],
    )

    assert _ids(tulip) == {"add", "subtract", "multiply", "divide", "slow", "speak"}


def test_load_instance(tool_library_factory):
    calculator = Calculator(divisor=3)
    tulip = tool_library_factory()

    tulip.load_functions_from_instance(instance=calculator)

    assert _ids(tulip) == {"add", "custom_division"}


def test_load_callables(tool_library_factory):
    tulip = tool_library_factory()

    tulip.load_functions_from_callables(functions=[example_tools.multiply])

    assert _ids(tulip) == {"multiply"}


def test_load_name_clash(tool_library_factory):
    calculator = Calculator(divisor=3)
    tulip = tool_library_factory(file_imports=[("tests.example_tools", ["add"])])

    with pytest.raises(ValueError):
        tulip.load_functions_from_instance(instance=calculator)


def test_load_names_from_file(tool_library_factory):
    tulip = tool_library_factory(
        file_imports=[("tests.example_tools", ["multiply"])],
    )

    assert _ids(tulip) == {"multiply"}


def test_init_mcp_reloads_from_disk(tool_library_factory, monkeypatch):
    _patch_mcp_manager(monkeypatch, [_mcp_tool_definition("disk_mcp_tool")])
    mcp_config = _mcp_config()

    first = tool_library_factory(
        chroma_sub_dir="mcp_reload/",
        mcp_imports=[(mcp_config, [])],
    )
    assert "disk_mcp_tool" in first.tools

    monkeypatch.setattr(
        ToolLibrary, "_load_mcp_function_definitions", lambda *_, **__: []
    )
    second = tool_library_factory(
        chroma_sub_dir="mcp_reload/",
        mcp_imports=[(mcp_config, [])],
    )

    assert "disk_mcp_tool" in second.tools


def test_mcp_tool_uses_manager():
    mcp_config = _mcp_config()
    manager = FakeMcpClientManager([_mcp_tool_definition("ping")])
    config_key = McpTool.serialized_config(mcp_config)
    definitions = manager.list_tools(config_key, mcp_config)
    tool_names = {t.name for t in definitions}
    assert "ping" in tool_names

    ping_meta = next(t for t in definitions if t.name == "ping")
    ping_definition = {
        "type": "function",
        "function": {
            "name": ping_meta.name,
            "description": ping_meta.description or "",
            "parameters": ping_meta.inputSchema,
        },
        "strict": True,
    }
    ping_tool = McpTool(
        mcp_config=mcp_config,
        function_name="ping",
        definition=ping_definition,
        mcp_manager=manager,
    )

    assert ping_tool(text="pong") == "pong"


def test_init_mcp_reloads_selected_function_names_from_disk(
    tool_library_factory,
    monkeypatch,
):
    _patch_mcp_manager(
        monkeypatch,
        [_mcp_tool_definition("alpha"), _mcp_tool_definition("beta")],
    )
    mcp_config = _mcp_config()

    first = tool_library_factory(
        chroma_sub_dir="mcp_subset/",
        mcp_imports=[(mcp_config, ["beta"])],
    )
    assert "beta" in first.tools
    assert "alpha" not in first.tools

    monkeypatch.setattr(
        ToolLibrary, "_load_mcp_function_definitions", lambda *_, **__: []
    )
    second = tool_library_factory(
        chroma_sub_dir="mcp_subset/",
        mcp_imports=[(mcp_config, ["beta"])],
    )

    assert "beta" in second.tools
    assert "alpha" not in second.tools


def test_search_function(tool_library_factory):
    tulip = tool_library_factory(file_imports=[("tests.example_tools", [])])

    res = tulip.search(problem_description="add 4 and 5", top_k=1)

    assert res[0].unique_id == "add"


def test_search_respects_similarity_threshold(tool_library_factory):
    tulip = tool_library_factory(file_imports=[("tests.example_tools", [])])

    res = tulip.search(
        problem_description="add 4 and 5",
        top_k=1,
        similarity_threshold=-1,
    )

    assert res == []


def test_remove_tool(tool_library_factory):
    tulip = tool_library_factory(file_imports=[("tests.example_tools", [])])

    tulip.remove_tool(tool_id="add")

    assert _ids(tulip) == {"subtract", "multiply", "divide", "slow", "speak"}


def test_remove_tools_by_instance(tool_library_factory):
    calculator = Calculator(divisor=3)
    tulip = tool_library_factory(instance_imports=[calculator])

    tulip.remove_tools_by_instance(instance=calculator)

    assert len(_ids(tulip)) == 0


def test_update_tool(tool_library_factory, tmp_path, monkeypatch):
    module_name = "example_module_for_update"
    module_path = tmp_path / f"{module_name}.py"
    module_path.write_text(_example_module_code("return text"), encoding="utf-8")
    sys.modules.pop(module_name, None)
    monkeypatch.syspath_prepend(str(tmp_path))
    tulip = tool_library_factory(file_imports=[(module_name, [])])
    function_id = "example"

    initial_res = execute_parallel_jobs(
        jobs=[
            Job(
                tool_call_id=function_id,
                tool=tulip.tools[function_id],
                parameters={"text": "unchanged"},
            )
        ]
    )
    assert initial_res[0].result.error is None
    assert initial_res[0].result.value == "unchanged"

    Path(tulip.tools[function_id].module_path).write_text(
        _example_module_code('return "success"'),
        encoding="utf-8",
    )

    tulip.update_tool(tool_id=function_id)
    updated_res = execute_parallel_jobs(
        jobs=[
            Job(
                tool_call_id=function_id,
                tool=tulip.tools[function_id],
                parameters={"text": "failure"},
            )
        ]
    )
    assert updated_res[0].result.error is None
    assert updated_res[0].result.value == "success"


def _ids(tulip: ToolLibrary) -> set[str]:
    return set(tulip.collection.get(include=[])["ids"])


def _mcp_config() -> dict:
    return {
        "mcpServers": {
            "local": {
                "transport": "stdio",
                "command": "fake-mcp-server",
                "args": [],
            }
        }
    }


def _patch_mcp_manager(monkeypatch, tool_definitions: list[SimpleNamespace]) -> None:
    import tulip_agent.tool_library as tool_library_module

    monkeypatch.setattr(
        tool_library_module,
        "McpClientManager",
        lambda: FakeMcpClientManager(tool_definitions),
    )


def _example_module_code(return_statement: str) -> str:
    return (
        "def example(text: str) -> str:\n"
        '    """\n'
        "    Returns the input.\n"
        "\n"
        "    :param text: Input text.\n"
        "    :return: The input text.\n"
        '    """\n'
        f"    {return_statement}\n"
    )


def _mcp_tool_definition(name: str) -> SimpleNamespace:
    return SimpleNamespace(
        name=name,
        description=f"{name} description",
        inputSchema={
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    )


class FakeMcpClientManager:
    def __init__(self, tool_definitions: list[SimpleNamespace]) -> None:
        self.tool_definitions = tool_definitions

    def list_tools(self, config_key: str, mcp_config: dict) -> list[SimpleNamespace]:
        return self.tool_definitions

    def call_tool(
        self,
        config_key: str,
        mcp_config: dict,
        function_name: str,
        parameters: dict,
    ) -> str:
        return parameters["text"]
