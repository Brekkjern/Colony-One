from Components.renderer import Renderer
import pygame
from typing import Tuple
import common

class UILabel(object):

    def __init__(self, screen_location: Tuple[int, int], renderer: Renderer, font, text: str):
        self.screen_location = screen_location
        self.renderer = renderer
        self.font = font
        self.text = text

    def update(self):
        self.renderer.texture = self.font.render(self.text, True, common.color["black"])
