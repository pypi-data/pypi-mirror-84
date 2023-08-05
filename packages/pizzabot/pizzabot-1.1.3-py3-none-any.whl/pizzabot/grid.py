from dataclasses import dataclass


@dataclass
class PizzabotGrid:
    """
    A class to hold the grid passed in via the cli
    """

    x: int
    y: int
