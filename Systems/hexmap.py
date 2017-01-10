import math
from collections import namedtuple
from typing import List, Set

from common import Point, lerp

Orientation = namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
orientation_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0,
                                 0.0, 2.0 / 3.0, 0.5)

class Axial(namedtuple("_Axial", ["q", "r", "s"])):
    """ Object representing a point in cubic space.

    Object representing a point in cubic space.
    Any co-ordinate should always resolve to (q + r + s == 0).
    """

    def __new__(cls, q: int, r: int, s: int = None):
        """Create cubic object
        Requires (q + r + s == 0)
        :param q: First co-ordinate
        :param r: Second co-ordinate
        :param s: Third co-ordinate. If not given, it is calculated to the value of (-q -s)
        """

        if s is None:
            s = -q - r

        if not (isinstance(q, int) and isinstance(r, int) and isinstance(s, int)):
            raise ValueError("Invalid co-ordinates. Values are not integers.")

        if q + r + s != 0:
            raise ValueError("Invalid co-ordinates. Sum is not 0")

        return super().__new__(cls, q, r, s)

    def __eq__(self, other) -> bool:
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __add__(self, other) -> 'Axial':
        return Axial(self.q + other.q, self.r + other.r, self.s + other.s)

    def __sub__(self, other) -> 'Axial':
        return Axial(self.q - other.q, self.r - other.r, self.s - other.s)

    def __mul__(self, other: float) -> 'Axial':
        return TileMap.round_axial(self.q * other, self.r * other, self.s * other)

    def __hash__(self) -> int:
        return hash((self.q, self.r))

    def __repr__(self) -> str:
        return "Axial({0}, {1}, {2})".format(self.q, self.r, self.s)

    def __str__(self) -> str:
        return "q: {0}\tr: {1}\ts: {2}".format(self.q, self.r, self.s)

    def get_tuple(self) -> Point:
        """ Helper method returning tuple of first and second coordinate """
        return Point(self.q, self.r)

    def move(self, position: 'Axial') -> 'Axial':
        self.q = position.q
        self.r = position.r
        self.s = position.s
        return self


    @staticmethod
    def vector_length(vector: 'Axial') -> float:
        """ Scalar of an axial vector """
        return (abs(vector.q) + abs(vector.r) + abs(vector.s)) // 2

    def distance(self, end: 'Axial') -> float:
        """ Calculate scalar between two vectors """
        return self.vector_length(self - end)

    def pixel_position(self) -> Point:
        """ Find pixel self of hex """
        x = (orientation_pointy.f0 * self.q + orientation_pointy.f1 * self.r)
        y = (orientation_pointy.f2 * self.q + orientation_pointy.f3 * self.r)
        return Point(x, y)


class Hex(Axial):
    """ Object representing a hex on a map. Extends Axial.

    Object representing a hex on a map. Extends Axial.
    Any co-ordinate should always resolve to (q + r + s == 0).
    """

    # TODO: Remove hexes. Use composition on hex container objects instead.

    def __new__(cls, q: int, r: int, s: int = None, transparent: bool = True, passable: bool = True):
        obj = super().__new__(cls, q, r, s)
        obj.transparent = transparent
        obj.passable = passable
        return obj

    def __repr__(self) -> str:
        return "Hex({0}, {1}, {2}, transparent = {3}, passable = {4})".format(self.q, self.r, self.s, self.transparent,
                                                                              self.passable)

    def __str__(self) -> str:
        return "q: {0}\tr: {1}\ts: {2}\ttransparent: {3}\tpassable: {4}".format(self.q, self.r, self.s,
                                                                                self.transparent, self.passable)


class TileMap(object):
    """ Class handling game map """

    # Helper tuple for use in __cube_lerp
    TupleAxial = namedtuple("TupleAxial", ["q", "r", "s"])

    # Helper table to find axial neighbours
    directions = [Axial(+1, 0), Axial(+1, -1), Axial(0, -1), Axial(-1, 0), Axial(-1, +1), Axial(0, +1)]

    def __init__(self, table: dict = None):
        if table:
            self.table = table
        else:
            self.table = dict()

    def __iter__(self):
        return iter(self.table)

    # TODO: Use getter/setter on self.table instead of functions
    def add_hex_to_map(self, item: object, location: Axial) -> 'TileMap':
        """ Add hex to coordinate table. Ignores call if it already exists. """
        item_tuple = location.get_tuple()
        if item_tuple not in self.table:
            self.table[item_tuple] = item

        return self

    def get_hex_from_map(self, axial: Axial) -> 'Tile':
        """ Gets the hex in the co-ordinate slot of the axial """
        return self.table[axial.get_tuple()]

    @staticmethod
    def round_axial(q: float, r: float, s: float = None) -> Axial:
        """Accepts coordinates as floats and rounds them to the closest valid coordinates as integers. """
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

    def get_axial_neighbour_coordinate(self, coordinate: Axial, direction: int) -> Axial:
        """ Get the coordinate of a neighbouring hex
        Direction 0 is right. Direction 3 is left.
        Accepts integer modulo 6 representing the direction.
        """
        return coordinate + self.directions[(direction % 6)]

    def __cube_lerp(self, start: TupleAxial, end: TupleAxial, step: float) -> Axial:
        """ Lerp a cube co-ordinate """
        return self.round_axial(lerp(start.q, end.q, step), lerp(start.r, end.r, step), lerp(start.s, end.s, step))

    def __hex_corner_offset(self, corner: int) -> Point:
        """ Calculate offset of corner """
        angle = 2.0 * math.pi * (orientation_pointy.start_angle - corner) / 6
        return Point(math.cos(angle), math.sin(angle))

    def pixel_to_hex(self, location: Point) -> Axial:
        """ Finds the Axial value of a square point """
        q = orientation_pointy.b0 * location.x + orientation_pointy.b1 * location.y
        r = orientation_pointy.b2 * location.x + orientation_pointy.b3 * location.y
        return self.round_axial(q, r)

    def hex_corner_list(self, coordinate: Axial) -> List[Point]:
        """ Pixel co-ordinates of hex corners """
        corners = []
        center = coordinate.pixel_position()
        for i in range(0, 5):
            offset = self.__hex_corner_offset(i)
            corners.append(Point(center.x + offset.x, center.y + offset.y))

        return corners

    def draw_line(self, start: Axial, end: Axial) -> List[Axial]:
        """ Draw line from tuple to destination

        Draws a line from itself to another Axial co-ordinate.
        Returns a list of Axial co-ordinates intersecting co-ordinates.
        Co-ordinates are nudged slightly to make the line more consistent
        """
        distance = start.distance(end)
        start_nudge = self.TupleAxial(start.q + 0.000001, start.r + 0.000001, start.s - 0.000002)
        end_nudge = self.TupleAxial(end.q + 0.000001, end.r + 0.000001, end.s - 0.000002)
        step = 1.0 / max(distance, 1)

        results = []
        for i in range(0, distance + 1):
            results.append(self.__cube_lerp(start_nudge, end_nudge, step * i))

        return results

    @staticmethod
    def draw_range(center: Axial, radius: int) -> List[Axial]:
        """ Find all coordinates within distance from center """
        results = []
        for dx in range(-radius, radius + 1):
            min_range = max(-radius, -dx - radius)
            max_range = min(radius, (-dx + radius))
            for dy in range(min_range, max_range + 1):
                results.append(center + Axial(dx, dy))

        return results

    def draw_circle(self, center: Axial, radius: int) -> List[Axial]:
        """ Draw a circle on the map """

        results = []

        # Return only center if range is 0.
        if radius == 0:
            results.append(center)
            return results

        cube = center + (self.get_axial_neighbour_coordinate(center, 4) * radius)

        for direction in range(0, 6):
            for side in range(0, radius + 1):
                results.append(cube)
                cube = self.get_axial_neighbour_coordinate(cube, direction)

        return results

    def draw_spiral(self, center: Axial, radius: int) -> List[Axial]:
        """ Draw a spiral on the map """

        results = [center]
        for step in range(1, radius):
            results += self.draw_circle(center, step)

        return results

    def draw_available_movement(self, start: Axial, distance: int) -> Set['Tile']:
        """ Return a set of possible tiles to move to from start point """
        visited = set().add(self.get_hex_from_map(start))
        fringes = [self.get_hex_from_map(start)]

        for i in range(1, distance + 1):
            fringes.append([])
            for cube in fringes[i - 1]:
                for direction in range(0, 6):
                    neighbour = self.get_hex_from_map(self.get_axial_neighbour_coordinate(cube, direction))
                    # TODO: Tiles do not have the passable property that the Hex class had.
                    if neighbour not in visited and neighbour.passable:
                        visited.add(neighbour)
                        fringes[i].append(neighbour)

        return visited

    def draw_field_of_view(self, center: Axial, radius: int) -> List['Tile']:
        """ Return a list of all tiles that can be seen from center """
        results = []

        circle = self.draw_circle(center, radius)

        for point in circle:
            line = self.draw_line(center, point)
            for axial in line:
                line_hex = self.get_hex_from_map(axial)
                if line_hex not in results:
                    results.append(line_hex)
                    # TODO: Tiles do not have the transparency property that the Hex class had.
                    if not line_hex.transparent:
                        break

        return results

    @staticmethod
    def get_intersecting_range(range_a: list, range_b: list) -> Set[Axial]:
        """ Finds overlapping co-ordinates from two ranges """
        return set(range_a).intersection(range_b)
