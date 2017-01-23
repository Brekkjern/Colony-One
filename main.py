import math
import pygame
import pygame.locals
import common
import sys

import Systems.hexmap as hexmap
import Systems.renderer as renderer

import Entities.tile
import Entities.uilabel

from Components.renderer import Renderer as CompRenderer

def load_tile_table(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, math.floor(image_width / width)):
        line = []
        tile_table.append(line)
        for tile_y in range(0, math.floor(image_height / height)):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))

    return tile_table

sys_renderer = renderer.Renderer(common.Point(800,600),background_colour=common.color["white"])

table = load_tile_table("Tileset_Hexagonal_PointyTop_60x52_60x80.png", 60, 80)
tile_graphic = table[2][1]

m = hexmap.TileMap()
tile_size = common.Point(34, 25)


i = 0
for location in m.draw_range(hexmap.Axial(0, 0), 3):
    tile = Entities.tile.Tile(i, location, CompRenderer(location, 0, tile_graphic, common.Point(0,0), tile_size))
    m.add_hex_to_map(tile, tile.location)

    i += 1

loc = m.get_hex_from_map(hexmap.Axial(-1, -1))
loc.renderer.texture = table[1][1]
loc.renderer.rendering_layer = 2

sys_font = pygame.font.SysFont('Arial', 20)

label = Entities.uilabel.UILabel((50,50), CompRenderer(), sys_font, "Test text")



while pygame.event.wait().type != pygame.locals.QUIT:
    sys_renderer.render()
else:
    pygame.quit()
    sys.exit()