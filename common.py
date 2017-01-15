from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


def lerp(start: float, end: float, step: float) -> float:
    """ Linear interpolation helper function """
    return start + (end - start) * step


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)
