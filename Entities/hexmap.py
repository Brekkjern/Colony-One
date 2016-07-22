import math
import collections

Point = collections.namedtuple("Point", ["x", "y"])

# Statics for use in calculating between hex and pixel values
Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
layout_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0,
                            math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)

class Axial(object):
    def __init__(self, q: float, r: float, s: float = None):

        # Calculate s if there are only 2 arguments given.
        if not s:
            s = -q - r

        # Round values to get coordinates as integers
        rq = round(q)
        rr = round(r)
        rs = round(s)

        x_diff = abs(rq - q)
        y_diff = abs(rr - r)
        z_diff = abs(rs - s)

        if x_diff > y_diff and x_diff > z_diff:
            rq = -rr - rs
        elif y_diff > z_diff:
            rr = -rq - rs
        else:
            rs = -rq - rr

        # Make sure coordinates sum to 0
        assert (rq + rr + rs == 0)

        self.q = rq
        self.r = rr
        self.s = rs

    def __eq__(self, other) -> bool:
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __add__(self, other):
        return Axial(self.q + other.q, self.r + other.r, self.s + other.s)

    def __sub__(self, other):
        return Axial(self.q - other.q, self.r - other.r, self.s - other.s)

    def __mul__(self, other):
        return Axial(self.q * other, self.r * other, self.s * other)

    @staticmethod
    def vector_length(vector) -> int:
        return (abs(vector.q) + abs(vector.r) + abs(vector.s)) // 2

    def distance(self, other) -> int:
        return self.vector_length(self - other)

    def get_neighbour_coordinate(self, direction: int):
        direction %= 6
        dir_object = directions[direction]
        return Axial(self.q + dir_object.q, self.r + dir_object.r)

    @staticmethod
    def __lerp(a: float, b: float, step: float) -> int:
        return a + (b - a) * step

    def __cube_lerp(self, other, step):
        return Axial(self.__lerp(self.q, other.q, step),
                     self.__lerp(self.r, other.r, step),
                     self.__lerp(self.s, other.s, step))

    def drawline(self, other) -> list:
        N = self.distance(other)
        self_nudge = Axial(self.q + 0.000001, self.r + 0.000001, self.s - 0.000002)
        other_nudge = Axial(other.q + 0.000001, other.r + 0.000001, other.s - 0.000002)
        step = 1.0 / max(N, 1)

        results = []
        for i in range(0, N + 1):
            results.append(self_nudge.__cube_lerp(other_nudge, step * i))

        return results

    @staticmethod
    def __unpack_layout(layout) -> tuple:
        return (layout.orientation, layout.size, layout.origin)

    def hex_to_pixel(self, layout: Layout) -> Point:
        orientation, size, origin = self.__unpack_layout(layout)
        x = (orientation.f0 * self.q + orientation.f1 * self.r) * size.x
        y = (orientation.f2 * self.q + orientation.f3 * self.r) * size.y
        return Point(x + origin.x, y + origin.y)

    def hex_range(self, distance: int) -> list:
        results = []
        for dx in range(-distance, distance + 1):
            min_range = max(-distance, -dx - distance)
            max_range = min(distance, (-dx+ distance))
            for dy in range(min_range, max_range + 1):
                dz = -dx - dy
                results.append(self + Axial(dx, dy, dz))

        return results

# Helper table to find axial neighbours
directions = [Axial(+1, 0), Axial(+1, -1), Axial(0, -1), Axial(-1, 0), Axial(-1, +1), Axial(0, +1)]


class Hex(Axial):
    def __init__(self, q: float, r: float, s: float = None):
        super(Hex, self).__init__(q, r, s)

    def hex_corner_offset(self, layout: Layout, corner: int) -> Point:
        angle = 2.0 * math.pi * (layout.orientation.start_angle - corner) / 6
        return Point(layout.size.x * math.cos(angle), layout.size.y * math.sin(angle))

    def hex_corner_list(self, layout: Layout) -> list:
        corners = []
        center = self.hex_to_pixel(layout)
        for i in range(0, 5):
            offset = self.hex_corner_offset(layout, i)
            corners.append(Point(center.x + offset.x, center.y + offset.y))

        return corners


class Map(object):
    def __init__(self, table: dict):
        if not table:
            table = {}

        self.table = table

    def __hash_coord(self, item: Axial) -> int:
        return hash((item.q, item.r))

    def add_hex(self, item: Hex) -> bool:
        if not self.table[self.__hash_coord(item)]:
            self.table[self.__hash_coord(item)] = item
            return True
        else:
            return False

    def get_hex_from_axial(self, item: Axial) -> Hex:
        return self.table[self.__hash_coord(item)]

    @staticmethod
    def __unpack_layout(layout) -> tuple:
        return (layout.orientation, layout.size, layout.origin)

    def pixel_to_hex(self, layout, point: Point):
        orientation, size, origin = self.__unpack_layout(layout)
        pt = Point((point.x - origin.x) / size.x, (point.y - origin.y) / size.y)
        q = orientation.b0 * pt.x + orientation.b1 * pt.y
        r = orientation.b2 * pt.x + orientation.b3 * pt.y
        return Axial(q, r)