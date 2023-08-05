import re

from pizzabot.grid import PizzabotGrid
from pizzabot.coordinates import PizzabotCoordinate


GRID_REGEX = r"^-?\d+x-?\d+ \("
INTEGERS_REGEX = r"-?\d+"
SPLIT_PAIRS_BRACKET = r"\("


class PizzabotInput(object):
    """
    A class to parse a string with a grid and coordinates into
    object for the pizzabot to act on

    ...

    Attributes
    ----------
    order : int
        number of expected points in a coordinate

    coordinates : list
        List of PizzabotCoordinates for the pizzabot to deliver to

    grid : PizzabotGrid
        Grid pizzabot can travel on

    Methods
    -------
    _extract_grid():
        Extracts grid from the input string

    _extract_coordinates():
        Extracts coordinates from the input string

    _parse_coordinate():
        Return pizzabot coordinate from a inter bracket string

    _validate_coordinates():
        Returns true if the number of opening and closing braces match
        the number of found coordinates, as the regexes are based on braces
    """

    def __init__(self, input_string):
        self.order = 2
        self.grid = self._extract_grid(input_string)
        self.coordinates = self._extract_coordinates(input_string)

    def _extract_grid(self, input_string):
        if re.match(GRID_REGEX, input_string) == None:
            return None
        g_strs = re.findall(INTEGERS_REGEX, input_string)[: self.order]
        g_ints = [int(x) for x in g_strs]
        return PizzabotGrid(*g_ints)

    def _extract_coordinates(self, input_string):
        coordinates = []
        c_strs = re.split(SPLIT_PAIRS_BRACKET, input_string)
        if len(c_strs) < 1:
            return []
        for c_str in c_strs[1:]:
            coordinates.append(self._parse_coordinate(c_str))
        if self._validate_coordinates(input_string, coordinates):
            return coordinates
        return []

    def _parse_coordinate(self, c_str):
        strings = re.findall(INTEGERS_REGEX, c_str)[-self.order :]
        c_int_list = [int(x) for x in strings]
        return PizzabotCoordinate(*c_int_list)

    def _validate_coordinates(self, input_string, coordinates):
        count_open_brace = 0
        count_close_brace = 0
        for letter in input_string:
            if letter == "(":
                count_open_brace += 1
            if letter == ")":
                count_close_brace += 1
        if count_open_brace == count_close_brace == len(coordinates):
            return True
        return False
