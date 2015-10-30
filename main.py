from Entities.structure import Structure
from Entities.colonist import Colonist
from Entities.colony import Colony

tick = 0

# Game difficulty modifiers
game_settings = {'year': 365, 'morale': 0.5}

print("DEBUG: Create Colony.")
test_colony = Colony(game_settings)

for i in range(0, 10):
    print("DEBUG: Add colonists to colony.")
    test_colony.new_colonist()
    i += 1

for i in range(0, 10):
    print("DEBUG: Add structure to colony.")
    test_colony.new_building()
    i += 1

while test_colony.colonists:
    tick += 1
    test_colony.update(tick)

