#!/usr/bin/env python3
import copy

from tulip_agent import Task, Tool


# placeholder tools
def mix_a_margherita_tool():
    pass


def prepare_a_pineapple_pizza_tool():
    pass


def turn_on_the_radiator_tool():
    pass


def generated_tool():
    pass


def run_example():
    q = "mix a margherita, prepare a pineapple pizza, and turn on the radiator"
    t0 = Task(description=q)
    print(t0.__dict__)
    # eg, no tools found, decompose further
    subtask_descriptions = [
        "mix a margherita",
        "prepare a pineapple pizza",
        "turn on the radiator",
    ]
    subtasks = [Task(description=d, supertask=t0) for d in subtask_descriptions]
    for s1, s2 in zip(subtasks, subtasks[1:]):
        s1.successor = s2
        s2.predecessor = s1
    s2b = copy.copy(subtasks[1])
    s2b.description += " variant"
    subtasks[1].paraphrased_variants = [s2b]
    # TODO: predecessor and validation example
    for c, s in enumerate(subtasks):
        s.tool_candidates = [
            Tool(
                function_name=f"{s.description.replace(' ', '_')}_tool",
                module_name="task_tree_example",
                definition={"function": {"description": "dummy"}},
                predecessor=(
                    subtasks[c - 1].tool_candidates[0].unique_id if c == 1 else None
                ),
            )
        ]
    subtasks[0].generated_tools.append(
        Tool(
            function_name="generated_tool",
            module_name="task_tree_example",
            definition={"function": {"description": "dummy"}},
        )
    )
    t0.subtasks.append(subtasks)
    for st in subtasks:
        print(st.__dict__)
    print(t0.__dict__)
    t0.plot()
    valid = t0.validate()
    print(f"{valid=}")


if __name__ == "__main__":
    run_example()
