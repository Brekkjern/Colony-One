from collections import namedtuple
from typing import Union

NumAlias = Union[float, int]

Point = namedtuple("Point", ["x", "y"])

color = {"black": (0,0,0),
         "white": (255,255,255)}


def lerp(start: float, end: float, step: float) -> float:
    """ Linear interpolation helper function """
    return start + (end - start) * step


def clamp(value: NumAlias, min_value: NumAlias, max_value: NumAlias) -> NumAlias:
    """ Clamps a value between a minimum and maximum value.

    Errors if the minimum value is larger than the maximum.
    """

    if min_value > max_value:
        raise ValueError("Minimum value can't be larger than maximum value.")

    return max(min(value, max_value), min_value)
