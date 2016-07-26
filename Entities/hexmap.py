import math
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


class Axial(namedtuple("_Axial", ["q", "r", "s"])):
    """ Object representing a point in cubic space.

    Object representing a point in cubic space.
    Any co-ordinate should always resolve to (q + r + s == 0).
    """

    def __new__(cls, q: int, r: int, s: int = None):
        """ Create cubic object

        Errors if (q + r + s != 0)

        :param q: First co-ordinate
        :type q: int
        :param r: Second co-ordinate
        :type r: int
        :param s: Third co-ordinate. If not given, it is calculated to -q -s
        :type s: int
        """

        # Calculate s if there are only 2 arguments given.
        if s is None:
            s = -q - r

        # Checks if variables are ints
        if not (isinstance(q, int) and isinstance(r, int) and isinstance(s, int)):
            raise ValueError("Invalid co-ordinates. Values are not integers.")

        # Make sure coordinates sum to 0
        if q + r + s != 0:
            raise ValueError("Invalid co-ordinates. Sum is not 0")

        return super().__new__(cls, q, r, s)

    def __eq__(self, other) -> bool:
        """ Check if another point is in same location

        :param other: The other object to compare with
        :type other: Axial
        :return: True if co-ordinates are the same
        :rtype: bool
        """
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __add__(self, other):
        """ Add two axial objects together

        :param other: Axial to add
        :type other: Axial
        :return: Axial of new location
        :rtype: Axial
        """
        return Axial(self.q + other.q, self.r + other.r, self.s + other.s)

    def __sub__(self, other):
        """ Subtract two axial objects from each other

        :param other: Axial to subtract
        :type other: Axial
        :return: Axial of new location
        :rtype: Axial
        """
        return Axial(self.q - other.q, self.r - other.r, self.s - other.s)

    def __mul__(self, other: int):
        """ Multiply co-ordinates of axial

        :param other: Number to multiply with
        :type other: int, float
        :return: Axial of new location
        :rtype: Axial
        """
        return Map.round_axial(self.q * other, self.r * other, self.s * other)

    def __hash__(self) -> int:
        """ Hashes a tuple of the two first values of the co-ordinate

        :return: Hash value of two first co-ordinate values
        :rtype: int
        """
        return hash((self.q, self.r))


class Hex(Axial):
    """ Object representing a hex on a map. Extends Axial.

    Object representing a hex on a map. Extends Axial.
    Any co-ordinate should always resolve to (q + r + s == 0).
    """

    def __new__(cls, q: int, r: int, s: int = None):
        """ Initialise Hex object

        Rounds to closest integers and errors if (q + r + s != 0)

        :param q: First co-ordinate
        :type q: int
        :param r: Second co-ordinate
        :type r: int
        :param s: Third co-ordinate. If not given, it is calculated to -q -s
        :type s: int
        """
        super().__new__(cls, q, r, s)


class Map(object):
    """ Class handling game map"""

    TupleAxial = namedtuple("TupleAxial", ["q", "r", "s"])
    Orientation = namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
    Layout = namedtuple("Layout", ["orientation", "size", "origin"])

    # Helper table to find axial neighbours
    directions = [Axial(+1, 0), Axial(+1, -1), Axial(0, -1), Axial(-1, 0), Axial(-1, +1), Axial(0, +1)]

    # Statics for use in calculating between hex and pixel values
    layout_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0,
                                0.0, 2.0 / 3.0, 0.5)

    def __init__(self, table: dict = None):
        """ Instantiates the map

        :param table: Optional table to load
        :type table: dict
        """
        if not table:
            table = {}

        self.table = table

    def add_hex_to_map(self, item: Hex) -> bool:
        """ Add hex to co-ordinate table

        Adds a hex to the co-ordinate table.
        Returns false if the co-ordinate is already occupied.

        :param item: Hex to add to table
        :type item: Hex
        :return: True if hex is added
        :rtype: bool
        """
        hashed_item = hash(item)
        if not self.table[hashed_item]:
            self.table[hashed_item] = item
            return True
        else:
            return False

    def get_hex_from_map(self, item: Axial) -> Hex:
        """ Gets the hex in the co-ordinate slot of the axial

        :param item: Co-ordinate object to get hex from
        :type item: Axial
        :return: Hexagon item
        :rtype: Hex
        """
        return self.table[hash(item)]

    @staticmethod
    def round_axial(q: float, r: float, s: float = None):
        """ Round values to get coordinates as integers

        :param q: First co-ordinate
        :type q: int, float
        :param r: Second co-ordinate
        :type r: int, float
        :param s: Third co-ordinate. Optional.
        :type s: int, float
        :return: Axial with int co-ordinates
        :rtype: Axial
        """
        if s is None:
            s = -q - r

        rq = round(q)
        rr = round(r)
        rs = round(s)

        q_diff = abs(rq - q)
        r_diff = abs(rr - r)
        s_diff = abs(rs - s)

        if q_diff > r_diff and q_diff > s_diff:
            rq = -rr - rs
        elif r_diff > s_diff:
            rr = -rq - rs
        else:
            rs = -rq - rr

        return Axial(int(rq), int(rr), int(rs))

    @staticmethod
    def vector_length(vector: Axial) -> float:
        """ Scalar of an axial vector

        :param vector: Axial to calculate
        :type vector: Axial
        :return: Distance to 0,0
        :rtype: int, float
        """
        return (abs(vector.q) + abs(vector.r) + abs(vector.s)) // 2

    def distance(self, start: Axial, end: Axial) -> int:
        """ Calculate scalar between two vectors

        :param start: First object for comparison
        :type start: Axial
        :param end: Second object for comparison
        :type end: Axial
        :return: Distance between objects
        :rtype: int
        """
        return self.vector_length(start - end)

    def get_axial_neighbour_coordinate(self, coordinate: Axial, direction: int):
        """ Get the co-ordinate of a neighbouring hex

        Finds the co-ordinate of a neighbouring hex.
        Direction 0 is right. Direction 3 is left.

        :param coordinate: Starting location
        :type coordinate: Axial
        :param direction: Neighbour direction. Int 0-5
        :type direction: int
        :return: Neighbouring hex
        :rtype: Axial
        """
        return coordinate + self.directions[(direction % 6)]

    @staticmethod
    def __lerp(start: float, end: float, step: float) -> float:
        """ Linear interpolation helper function

        :param start: Start value
        :type start: int, float
        :param end: Destination value
        :type end: int, float
        :param step: Size of step
        :type step: int, float
        :return: Current value
        :rtype: int, float
        """
        return start + (end - start) * step

    def __cube_lerp(self, start: TupleAxial, end: TupleAxial, step: float):
        """ Lerp a cube co-ordinate

        :param start: Start axial
        :type start: TupleAxial
        :param end: End axial
        :type end: TupleAxial
        :param step: Size of step
        :type step: int, float
        :return: Axial of current position in lerp
        :rtype: Axial
        """
        return self.round_axial(self.__lerp(start.q, end.q, step), self.__lerp(start.r, end.r, step),
                                self.__lerp(start.s, end.s, step))

    def draw_line(self, start: Axial, end: Axial) -> list:
        """ Draw line from tuple to destination

        Draws a line from itself to another Axial co-ordinate.
        Returns a list of Axial co-ordinates intersecting co-ordinates.
        Co-ordinates are nudged slightly to make the line more consistent

        :param start: Start of line
        :type start: Axial
        :param end: End of line
        :type end: Axial
        :return: List of Axial objects
        :rtype: list
        """
        distance = self.distance(start, end)
        start_nudge = self.TupleAxial(start.q + 0.000001, start.r + 0.000001, start.s - 0.000002)
        end_nudge = self.TupleAxial(end.q + 0.000001, end.r + 0.000001, end.s - 0.000002)
        step = 1.0 / max(distance, 1)

        results = []
        for i in range(0, distance + 1):
            results.append(self.__cube_lerp(start_nudge, end_nudge, step * i))

        return results

    @staticmethod
    def hex_to_pixel(coordinate: Axial, layout: Layout) -> Point:
        """ Find pixel co-ordinate of hex

        :param coordinate: Axial location to convert to 2D point
        :type coordinate: Axial
        :param layout: Pointy or flat-top layout
        :type layout: Layout
        :return: Square co-ordinate of hex
        :rtype: Point
        """
        orientation, size, origin = layout.orientation, layout.size, layout.origin
        x = (orientation.f0 * coordinate.q + orientation.f1 * coordinate.r) * size.x
        y = (orientation.f2 * coordinate.q + orientation.f3 * coordinate.r) * size.y
        return Point(x + origin.x, y + origin.y)

    def pixel_to_hex(self, layout: Layout, location: Point):
        """ Finds the Axial value of a square point

        :param layout: Pointy or flat-top layout
        :type layout: Layout
        :param location: Square point to calculate
        :type location: Point
        :return: Cubic location of input point
        :rtype: Axial
        """
        orientation, size, origin = layout.orientation, layout.size, layout.origin
        pt = Point((location.x - origin.x) / size.x, (location.y - origin.y) / size.y)
        q = orientation.b0 * pt.x + orientation.b1 * pt.y
        r = orientation.b2 * pt.x + orientation.b3 * pt.y
        return self.round_axial(q, r)

    @staticmethod
    def axial_range(center: Axial, distance: int) -> list:
        """ Find all coordinates within *distance*

        :param center: Center point of range
        :type center: Axial
        :param distance: Integer that describes search range
        :type distance: int
        :return: List of Axial objects within the range
        :rtype: list
        """
        results = []
        for dx in range(-distance, distance + 1):
            min_range = max(-distance, -dx - distance)
            max_range = min(distance, (-dx + distance))
            for dy in range(min_range, max_range + 1):
                dz = -dx - dy
                results.append(center + Axial(dx, dy, dz))

        return results

    @staticmethod
    def intersecting_range(range_a: list, range_b: list) -> set:
        """ Finds overlapping co-ordinates from two ranges

        :param range_a: List of axial points
        :type range_a: list
        :param range_b: List of axial points
        :type range_b: list
        :return: Set of points that are in both lists
        :rtype: set
        """
        return set(range_a).intersection(range_b)

    @staticmethod
    def __hex_corner_offset(layout: Layout, corner: int) -> Point:
        """ Calculate offset of corner

        :param layout: Pointy or flat-top layout
        :type layout: Layout
        :param corner: Direction of corner
        :type corner: int
        :return: Offset of corner
        :rtype: Point
        """
        angle = 2.0 * math.pi * (layout.orientation.start_angle - corner) / 6
        return Point(layout.size.x * math.cos(angle), layout.size.y * math.sin(angle))

    def hex_corner_list(self, coordinate: Axial, layout: Layout) -> list:
        """ Pixel co-ordinates of hex corners

        :param coordinate: Center point
        :type coordinate: Axial
        :param layout: Pointy or flat-top layout
        :type layout: Layout
        :return: List of point objects
        :rtype: list
        """
        corners = []
        center = self.hex_to_pixel(coordinate, layout)
        for i in range(0, 5):
            offset = self.__hex_corner_offset(layout, i)
            corners.append(Point(center.x + offset.x, center.y + offset.y))

        return corners

    def draw_circle(self, center: Axial, radius: int) -> list:
        """ Draw a circle on the map

        :param center: Center of the circle
        :type center: Axial
        :param radius: Radius of the circle
        :type radius: int
        :return: List of axial coordinates that make up the circle
        :rtype: list
        """

        # To avoid a multiply by zero issue, set radius to 1 instead of 0
        if radius == 0:
            radius = 1

        results = []

        cube = center + (self.get_axial_neighbour_coordinate(center, 4) * radius)

        for direction in range(0, 6):
            for side in range(0, radius + 1):
                results.append(cube)
                cube = self.get_axial_neighbour_coordinate(cube, direction)

        return results

    def draw_spiral(self, center: Axial, radius: int) -> list:
        """ Draw a spiral on the map

        :param center: Center of spiral
        :type center: Axial
        :param radius: Radius of spiral
        :type radius: int
        :return: Ordered list of axials
        :rtype: list
        """

        results = [center]
        for step in range(1, radius):
            results += self.draw_circle(center, step)

        return results
