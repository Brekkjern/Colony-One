import math
import collections

Point = collections.namedtuple("Point", ["x", "y"])
Axial = collections.namedtuple("Axial", ["q", "r", "s"])
Cube = collections.namedtuple("Cube", ["x", "y", "z"])


class Hex(object):

    directions = [
        Axial(+1, 0), Axial(+1, -1), Axial(0, -1),
        Axial(-1, 0), Axial(-1, +1), Axial(0, +1)
    ]

    def __init__(self, center: Axial, size: float):
        self.center = center
        self.size = size

    def get_hex_corner(self, corner_number: int) -> Point:
        """Returns point of hex corner

        Returns the point of the corner counted from the rightmost corner of the hex.

        :param corner_number: corner to return
        :return: Point object of corner
        """
        angle_deg = 60 * corner_number + 30
        angle_rad = math.pi / 180 * angle_deg

        return Point(self.center.q + self.size + math.cos(angle_rad), self.center.r + self.size + math.sin(angle_rad))

    def get_hex_neighbour(self, direction: int) -> Point:
        dir_object = self.directions[direction]
        return Point(self.center.q + dir_object.q, self.center.r + dir_object.r)


class Map(object):
    def __init__(self, table: dict):
        if not table:
            table = {}

        self.table = table

    def __hash_coord(self, x: int, y: int) -> int:
        return hash((x, y))

    def add_coord(self, x: int, y: int, item: object):
        self.table[self.__hash_coord(x, y)] = item

    def get_coord(self, x: int, y: int) -> object:
        return self.table[self.__hash_coord(x, y)]

    def _convert_to_cube(self, q: int, r: int) -> Cube:
        x = q
        z = r
        y = -x - z
        return Cube(x, y, z)

    def _cube_distance(self, a: Cube, b: Cube) -> int:
        return (abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)) / 2

    def get_distance(self, a: Axial, b: Axial) -> int:
        a_cube = self._convert_to_cube(a.q, a.r)
        b_cube = self._convert_to_cube(b.q, b.r)
        return self._cube_distance(a_cube, b_cube)

    def add_cube(self, a: Cube, b: Cube) -> Cube:
        return Cube(a.x + b.x, a.y + b.y, a.z + b.z)

    def cube_round(self, cube: Cube) -> Cube:
        rx = round(cube.x)
        ry = round(cube.y)
        rz = round(cube.z)

        x_diff = abs(rx - cube.x)
        y_diff = abs(ry - cube.y)
        z_diff = abs(rz - cube.z)

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry

        return Cube(rx, ry, rz)

    def lerp(self, a: float, b: float, t: float) -> int:
        return a + (b - a) * t

    def cube_lerp(self, a: Cube, b: Cube, t) -> Cube:
        return Cube(self.lerp(a.x, b.x, t), self.lerp(a.y, b.y, t), self.lerp(a.z, b.z, t))

    def cube_drawline(self, a: Cube, b: Cube) -> list:
        N = self._cube_distance(a, b)
        a_nudge = Cube(a.x + 0.000001, a.y + 0.000001, a.z - 0.000002)
        b_nudge = Cube(b.x + 0.000001, b.y + 0.000001, b.z - 0.000002)
        step = 1.0 / max(N, 1)

        results = []
        for i in range(0, N + 1):
            results.append(self.cube_round(self.cube_lerp(a_nudge, b_nudge, step * i)))

        return results

    def hex_range(self, center: Cube, distance: int) -> list:
        results = []
        for i in range(-distance, distance):
            # Todo: Finish this function
            pass
