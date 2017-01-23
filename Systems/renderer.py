from typing import Tuple

import pygame
import pygame.locals

from Components.renderer import Renderer as CompRender
from common import Point


class Renderer(object):
    def __init__(self, screen_size: Point, background_colour: Tuple[int, int, int]):
        self.screen_size = screen_size
        self.background = background_colour

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.screen_size.x, self.screen_size.y))
        self.screen.fill(self.background)

    def sort_components(self):
        CompRender.renderers.sort(key = lambda entry: (entry.get_pixel_location().x, entry.rendering_layer))

    def render_component(self):
        for component in CompRender.renderers:
            posx, posy = component.get_pixel_location()

            self.screen.blit(component.texture, (posx + (self.screen_size.x / 2), posy + (self.screen_size.y / 2)))

    def render(self):
        self.sort_components()
        self.render_component()
        pygame.display.flip()
