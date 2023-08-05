from pizzabot.input import PizzabotInput
from pizzabot.coordinates import PizzabotCoordinate
from pizzabot.instructions import PizzabotInstructions


class PizzabotEngine(object):
    """
    A class to calculate instructions from a string for the pizzabot to perform

    ...

    Attributes
    ----------
    instructions : PizzabotInstructions
        Instructions the pizzabot can perform

    position : PizzabotCoordinate
        The current position of the pizzabot

    journey : list
        Instructions performed by the pizzabot

    input : PizzabotInput
        Parses input string, to grid and coordinates objects

    Methods
    -------
    update_postion(target):
        Moves the pizzabot closer to the target by selecting the best
        instruction, records the best instruction to its journey.

    process_string(input_string):
        Takes a string from the CLI, encoding a grid and coordinates. Returns
        short hand notation for the pizzabot to deliver pizza to coordinates.
    """

    def __init__(self):
        self.instructions = PizzabotInstructions().Instructions
        self.position = PizzabotCoordinate(0, 0)
        self.journey = []
        self.input = None

    def update_postion(self, target):
        smallest_delta = abs(target - self.position)
        for instruction in self.instructions:
            delta = abs(target - instruction.movement - self.position)
            if delta < smallest_delta:
                best_instruction = instruction
                smallest_delta = delta
        self.journey.append(best_instruction)
        self.position += best_instruction.movement
        return best_instruction

    def process_string(self, input_string):
        output_string = ""
        self.input = PizzabotInput(input_string)
        if self.input.coordinates == []:
            return None
        for target in self.input.coordinates:
            while self.position != target:
                self.update_postion(target)
            self.journey.append(self.instructions[0])
        for step in self.journey:
            output_string += step.shorthand
        return output_string
