from Entities.colony import Colony
import conf

print("DEBUG: Create Colony.")
test_colony = Colony(conf.game_settings)

for i in range(0, 10):
    # print("DEBUG: Add colonists to colony.")
    test_colony.new_colonist()

for i in range(0, 10):
    print("DEBUG: Add structure to colony.")
    test_colony.new_building()

while test_colony.colonists:
    conf.tick += 1
    print(conf.tick)
    test_colony.update()

