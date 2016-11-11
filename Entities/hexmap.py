import math
from collections import namedtuple
from typing import List
from typing import Set

Point = namedtuple("Point", ["x", "y"])


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
        return Map.round_axial(self.q * other, self.r * other, self.s * other)

    def __hash__(self) -> int:
        return hash((self.q, self.r))

    def __repr__(self) -> str:
        return "Axial({0}, {1}, {2})".format(self.q, self.r, self.s)

    def __str__(self) -> str:
        return "q: {0}\tr: {1}\ts: {2}".format(self.q, self.r, self.s)

    def get_tuple(self) -> Point:
        """ Helper method returning tuple of first and second coordinate """
        return Point(self.q, self.r)

    @staticmethod
    def vector_length(vector: 'Axial') -> float:
        """ Scalar of an axial vector """
        return (abs(vector.q) + abs(vector.r) + abs(vector.s)) // 2

    def distance(self, end: 'Axial') -> int:
        """ Calculate scalar between two vectors """
        return self.vector_length(self - end)


class Hex(Axial):
    """ Object representing a hex on a map. Extends Axial.

    Object representing a hex on a map. Extends Axial.
    Any co-ordinate should always resolve to (q + r + s == 0).
    """

    #TODO: Remove hexes. Use composition on hex container objects instead.

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


class Map(object):
    """ Class handling game map """
    #TODO: Rename class. Name is too similar to the builtin map()
    TupleAxial = namedtuple("TupleAxial", ["q", "r", "s"])
    Orientation = namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
    Layout = namedtuple("Layout", ["orientation", "size", "origin"])

    # Helper table to find axial neighbours
    directions = [Axial(+1, 0), Axial(+1, -1), Axial(0, -1), Axial(-1, 0), Axial(-1, +1), Axial(0, +1)]

    # Statics for use in calculating between hex and pixel values
    orientation_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0,
                                     -1.0 / 3.0,
                                     0.0, 2.0 / 3.0, 0.5)

    def __init__(self, default_layout: Layout = None, table: dict = None):
        if default_layout:
            self.layout = default_layout
        else:
            self.layout = self.Layout(self.orientation_pointy, Point(1, 1), Point(0, 0))

        if not table:
            table = dict()

        self.table = table

    def __iter__(self):
        return iter(self.table)

    #TODO: Use getter/setter on self.table instead of functions
    def add_hex_to_map(self, item: Hex) -> bool:
        """ Add hex to coordinate table. Returns false if the co-ordinate is already occupied. """
        item_tuple = item.get_tuple()
        if item_tuple not in self.table:
            self.table[item_tuple] = item
            return True
        else:
            return False

    def get_hex_from_map(self, axial: Axial) -> Hex:
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

    @staticmethod
    def __lerp(start: float, end: float, step: float) -> float:
        """ Linear interpolation helper function """
        #TODO: Move to other file
        return start + (end - start) * step

    def __cube_lerp(self, start: TupleAxial, end: TupleAxial, step: float) -> Axial:
        """ Lerp a cube co-ordinate """
        return self.round_axial(self.__lerp(start.q, end.q, step), self.__lerp(start.r, end.r, step),
                                self.__lerp(start.s, end.s, step))

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

    def hex_to_pixel(self, coordinate: Axial, layout: Layout = None) -> Point:
        """ Find pixel coordinate of hex """
        if not layout:
            layout = self.layout

        orientation, size, origin = layout.orientation, layout.size, layout.origin
        x = (orientation.f0 * coordinate.q + orientation.f1 * coordinate.r) * size.x
        y = (orientation.f2 * coordinate.q + orientation.f3 * coordinate.r) * size.y
        return Point(x + origin.x, y + origin.y)

    def pixel_to_hex(self, location: Point, layout: Layout = None) -> Axial:
        """ Finds the Axial value of a square point """
        if not layout:
            layout = self.layout

        orientation, size, origin = layout.orientation, layout.size, layout.origin
        pt = Point((location.x - origin.x) / size.x, (location.y - origin.y) / size.y)
        q = orientation.b0 * pt.x + orientation.b1 * pt.y
        r = orientation.b2 * pt.x + orientation.b3 * pt.y
        return self.round_axial(q, r)

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

    @staticmethod
    def intersecting_range(range_a: list, range_b: list) -> Set[Axial]:
        """ Finds overlapping co-ordinates from two ranges """
        return set(range_a).intersection(range_b)

    @staticmethod
    def __hex_corner_offset(layout: Layout, corner: int) -> Point:
        """ Calculate offset of corner """
        angle = 2.0 * math.pi * (layout.orientation.start_angle - corner) / 6
        return Point(layout.size.x * math.cos(angle), layout.size.y * math.sin(angle))

    def hex_corner_list(self, coordinate: Axial, layout: Layout) -> List[Point]:
        """ Pixel co-ordinates of hex corners """
        corners = []
        center = self.hex_to_pixel(coordinate, layout)
        for i in range(0, 5):
            offset = self.__hex_corner_offset(layout, i)
            corners.append(Point(center.x + offset.x, center.y + offset.y))

        return corners

    def draw_circle(self, center: Axial, radius: int) -> List[Axial]:
        """ Draw a circle on the map """

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

    def draw_spiral(self, center: Axial, radius: int) -> List[Axial]:
        """ Draw a spiral on the map """

        results = [center]
        for step in range(1, radius):
            results += self.draw_circle(center, step)

        return results

    def get_field_of_view(self, center: Axial, radius: int) -> List[Hex]:
        """ Return a list of all tiles that can be seen from center """
        results = []

        circle = self.draw_circle(center, radius)

        for point in circle:
            line = self.draw_line(center, point)
            for axial in line:
                line_hex = self.get_hex_from_map(axial)
                if not line_hex in results:
                    results.append(line_hex)
                    if not line_hex.transparent:
                        break

        return results

    def draw_available_movement(self, start: Axial, distance: int) -> Set[Hex]:
        """ Return a set of possible tiles to move to from start point """
        visited = set().add(self.get_hex_from_map(start))
        fringes = []
        fringes.append(self.get_hex_from_map(start))

        for i in range(1, distance + 1):
            fringes.append([])
            for cube in fringes[i - 1]:
                for direction in range(0, 6):
                    neighbour = self.get_hex_from_map(self.get_axial_neighbour_coordinate(cube, direction))
                    if neighbour not in visited and neighbour.passable:
                        visited.add(neighbour)
                        fringes[i].append(neighbour)

        return visited
