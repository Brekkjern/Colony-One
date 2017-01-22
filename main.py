from Entities.hexmap import Axial
from Entities.hexmap import Map
from Entities.hexmap import Hex

tileMap = Map()
for tile in tileMap.draw_circle(Axial(0, 0), 10000):
    tile = Hex(tile.q, tile.r)
    tileMap.add_hex_to_map(tile)

# testAxial = Axial(1, 2)
# anotherAxial = Axial(5, -4)
#
# newAxial = testAxial + anotherAxial
# print(newAxial.q, newAxial.r)
#
# newAxial *= 3
# print(newAxial.q, newAxial.r)


