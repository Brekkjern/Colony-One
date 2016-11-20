import math
import weakref
from typing import List

from common import Point


class Renderer(object):
    # Table to hold all renderer components.
    renderers = []  # type: List['Renderer']

    def __init__(self, rendering_layer: int, texture, texture_center_offset: Point, size: Point):
        self.__class__.renderers.append(weakref.proxy(self))
        self.rendering_layer = rendering_layer
        self.texture = texture
        self.texture_center_offset = texture_center_offset
        self.size = size

    def prepare_render(self, pixel_location: Point) -> 'Renderer':
        self.pixel_location = pixel_location

        return self

    def get_pixel_location(self) -> Point:
        posx = math.floor((self.pixel_location.x + self.texture_center_offset.x) * self.size.x)
        posy = math.floor((self.pixel_location.y + self.texture_center_offset.y) * self.size.y)

        return Point(posx, posy)
