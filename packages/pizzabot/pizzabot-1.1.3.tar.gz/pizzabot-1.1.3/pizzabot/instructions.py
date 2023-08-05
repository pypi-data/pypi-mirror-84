from dataclasses import dataclass, field
from typing import List

from pizzabot.coordinates import PizzabotCoordinate as DeltaCord


"""
Add new instructions here
"""
shorthand_description_movement = [
    ("D", "Drop pizza", DeltaCord(0, 0)),
    ("N", "Move north", DeltaCord(0, 1)),
    ("S", "Move south", DeltaCord(0, -1)),
    ("E", "Move east", DeltaCord(1, 0)),
    ("W", "Move west", DeltaCord(-1, 0)),
]


@dataclass
class Instruction:
    """
    Defines an instruction

    ...
    Attributes
    shorthand : str
        Notation printed to the CLI referencing an instruction

    description: str
        The instruction in plain text

    movement: PizzabotCoordinate
        The change in coordinates following the pizzabot running
        instruction
    """

    shorthand: str
    description: str
    movement: DeltaCord


def make_instructions():
    """
    Build instructions from list
    """
    return [Instruction(s, d, m) for s, d, m in shorthand_description_movement]


@dataclass
class PizzabotInstructions:
    """
    Defines an instructions

    ...
    Attributes
    Instructions : List
        All instructions pizzabot can run.
    """

    Instructions: List[Instruction] = field(default_factory=make_instructions)
