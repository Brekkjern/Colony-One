import math
import weakref
from typing import List

from common import Point

from Systems.hexmap import Axial

class Renderer(object):
    # Table to hold all renderer components.
    renderers = []  # type: List['Renderer']

    def __init__(self, location: Axial, rendering_layer: int, texture, texture_center_offset: Point, size: Point):
        self.__class__.renderers.append(weakref.proxy(self))
        self.location = location
        self.rendering_layer = rendering_layer
        self.texture = texture
        self.texture_center_offset = texture_center_offset
        self.size = size

    def get_pixel_location(self) -> Point:
        pixel_location = self.location.pixel_position()
        posx = math.floor((pixel_location.x + self.texture_center_offset.x) * self.size.x)
        posy = math.floor((pixel_location.y + self.texture_center_offset.y) * self.size.y)

        return Point(posx, posy)
