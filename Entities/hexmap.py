import math
import collections

Point = collections.namedtuple("Point", ["x", "y"])
TupleAxial = collections.namedtuple("TupleAxial", ["q", "r", "s"])

# Statics for use in calculating between hex and pixel values
Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
layout_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0,
                            2.0 / 3.0, 0.5)


class Axial(object):
    """ Object representing a point in cubic space.

    Object representing a point in cubic space.
    Any co-ordinate should always resolve to (q + r + s == 0).
    """

    def __init__(self, q: int, r: int, s: int = None):
        """ Initialise cubic object

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
        if (q + r + s != 0):
            raise ValueError("Invalid co-ordinates. Sum is not 0")

        self.q = q
        self.r = r
        self.s = s

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

    def __mul__(self, other: float):
        """ Multiply co-ordinates of axial

        :param other: Number to multiply with
        :type other: int, float
        :return: Axial of new location
        :rtype: Axial
        """
        return Axial(self.q * other, self.r * other, self.s * other)

    def __hash__(self) -> int:
        """ Hashes a tuple of the two first values of the co-ordinate

        :return: Hash value of two first co-ordinate values
        :rtype: int
        """
        return hash((self.q, self.r))

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

        return Axial(rq, rr, rs)

    @staticmethod
    def vector_length(vector) -> float:
        """ Scalar of an axial vector

        :param vector: Axial to calculate
        :type vector: Axial
        :return: Distance to 0,0
        :rtype: int, float
        """
        return (abs(vector.q) + abs(vector.r) + abs(vector.s)) // 2

    def distance(self, other) -> float:
        """ Calculate scalar between self and vector

        :param other: Other vector
        :type other: Axial
        :return: Distance between objects
        :rtype: int, float
        """
        return self.vector_length(self - other)

    def get_neighbour_coordinate(self, direction: int):
        """ Get the co-ordinate of a neighbouring hex

        Finds the co-ordinate of a neighbouring hex.
        Direction 0 is right. Direction 3 is left.


        :param direction: Neighbour direction. Int 0-5
        :type direction: int
        :return: Neighbouring hex
        :rtype: Axial
        """
        direction %= 6
        dir_object = directions[direction]
        return self + dir_object

    @staticmethod
    def __lerp(a: float, b: float, step: float) -> float:
        """ Linear interpolation helper function

        :param a: Start value
        :type a: int, float
        :param b: Destination value
        :type b: int, float
        :param step: Size of step
        :type step: int, float
        :return: Current value
        :rtype: int, float
        """
        return a + (b - a) * step

    def __cube_lerp(self, a: TupleAxial, b: TupleAxial, step: float):
        """ Lerp a cube co-ordinate

        :param a: Start axial
        :type a: TupleAxial
        :param b: End axial
        :type b: TupleAxial
        :param step: Size of step
        :type step: int, float
        :return: Axial of current position in lerp
        :rtype: Axial
        """
        return self.round_axial(self.__lerp(a.q, b.q, step), self.__lerp(a.r, b.r, step), self.__lerp(a.s, b.s, step))

    def drawline(self, other) -> list:
        """ Draw line from tuple to destination

        Draws a line from itself to another Axial co-ordinate.
        Returns a list of Axial co-ordinates intersecting co-ordinates.
        Co-ordinates are nudged slightly to make the line more consistent

        :param other: End of line
        :type other: Axial
        :return: List of Axial objects
        :rtype: list
        """
        distance = self.distance(other)
        self_nudge = TupleAxial(self.q + 0.000001, self.r + 0.000001, self.s - 0.000002)
        other_nudge = TupleAxial(other.q + 0.000001, other.r + 0.000001, other.s - 0.000002)
        step = 1.0 / max(distance, 1)

        results = []
        for i in range(0, distance + 1):
            results.append(self.__cube_lerp(self_nudge, other_nudge, step * i))

        return results

    def hex_to_pixel(self, layout: Layout) -> Point:
        """ Find pixel co-ordinate of hex

        :param layout: Pointy or flat-top layout
        :type layout: Layout
        :return: Square co-ordinate of hex
        :rtype: Point
        """
        orientation, size, origin = layout.orientation, layout.size, layout.origin
        x = (orientation.f0 * self.q + orientation.f1 * self.r) * size.x
        y = (orientation.f2 * self.q + orientation.f3 * self.r) * size.y
        return Point(x + origin.x, y + origin.y)

    @staticmethod
    def pixel_to_hex(layout: Layout, location: Point):
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
        return Axial.round_axial(q, r)

    def hex_range(self, distance: int) -> list:
        """ Find all coordinates within *distance*

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
                results.append(self + Axial(dx, dy, dz))

        return results

    @staticmethod
    def intersecting_range(a: list, b: list) -> set:
        """ Finds overlapping co-ordinates from two ranges

        :param a: List of axial points
        :type a: list
        :param b: List of axial points
        :type b: list
        :return: Set of points that are in both lists
        :rtype: set
        """
        return set(a).intersection(b)


# Helper table to find axial neighbours
directions = [Axial(+1, 0), Axial(+1, -1), Axial(0, -1), Axial(-1, 0), Axial(-1, +1), Axial(0, +1)]


class Hex(Axial):
    """ Object representing a hex on a map. Extends Axial.

    Object representing a hex on a map. Extends Axial.
    Any co-ordinate should always resolve to (q + r + s == 0).
    """

    def __init__(self, q: float, r: float, s: float = None):
        """ Initialise Hex object

        Rounds to closest integers and errors if (q + r + s != 0)

        :param q: First co-ordinate
        :type q: int, float
        :param r: Second co-ordinate
        :type r: int, float
        :param s: Third co-ordinate. If not given, it is calculated to -q -s
        :type s: int, float
        """
        super(Hex, self).__init__(q, r, s)

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

    def hex_corner_list(self, layout: Layout) -> list:
        """ Pixel co-ordinates of hex corners

        :param layout: Pointy or flat-top layout
        :type layout: Layout
        :return: List of point objects
        :rtype: list
        """
        corners = []
        center = self.hex_to_pixel(layout)
        for i in range(0, 5):
            offset = self.__hex_corner_offset(layout, i)
            corners.append(Point(center.x + offset.x, center.y + offset.y))

        return corners


class Map(object):
    """ Class handling game map"""

    def __init__(self, table: dict = None):
        """ Instantiates the map

        :param table: Optional table to load
        :type table: dict
        """
        if not table:
            table = {}

        self.table = table

    @staticmethod
    def __hash_coord(item: Axial) -> int:
        """ Helper function to hash a co-ordinate value

        :param item: Axial to hash
        :type item: Axial
        :return: Hash value of co-ordinates
        :rtype: int
        """
        return hash((item.q, item.r))

    def add_hex(self, item: Hex) -> bool:
        """ Add hex to co-ordinate table

        Adds a hex to the co-ordinate table.
        Returns false if the co-ordinate is already occupied.

        :param item: Hex to add to table
        :type item: Hex
        :return: True if hex is added
        :rtype: bool
        """
        if not self.table[self.__hash_coord(item)]:
            self.table[self.__hash_coord(item)] = item
            return True
        else:
            return False

    def get_hex_from_axial(self, item: Axial) -> Hex:
        """ Gets the hex in the co-ordinate slot of the axial

        :param item: Co-ordinate object to get hex from
        :type item: Axial
        :return: Hexagon item
        :rtype: Hex
        """
        return self.table[self.__hash_coord(item)]