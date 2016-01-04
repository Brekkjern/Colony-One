from Entities.structure import Structure
from Entities.colonist import Colonist
import conf


class Colony(object):
    """Object model for Colony objects"""

    def __init__(self, game_settings, colonists=None, buildings=None, agridomes=None, generators=None):
        if not colonists:
            colonists = []

        if not buildings:
            buildings = []

        if not agridomes:
            agridomes = []

        if not generators:
            generators = []

        self.colonists = colonists
        self.buildings = buildings
        self.agridomes = agridomes
        self.generators = generators
        self.power = 0
        self.food = 0
        self.game_settings = game_settings

    def update(self):

        # Calculate what power is available
        self.calculate_power()

        alive_colonists = []

        for colonist in self.colonists:
            colonist.tick()
            colonist.update()

            # Add living colonists to table
            if not colonist.dead:
                alive_colonists.append(colonist)

        for building in self.buildings:
            if building.needs_power():
                if self.request_power(building.powered.active):
                    building.update()

        # Replace old table with new that only contains living colonists
        self.colonists = alive_colonists

    def request_power(self, power):
        # Drain a select amount of power from the colony if it's available.
        if self.power >= power:
            self.power -= power
            return True

        return False

    def new_colonist(self):
        colonist = Colonist(self.game_settings)
        self.colonists.append(colonist)
        return colonist

    def food_count(self):
        food = 0

        for agridome in self.agridomes:
            food += agridome.inventory

        return food

    def new_building(self):
        building = Structure()
        self.buildings.append(building)

        if building.__class__.__name__ == "Agridome":
            self.agridomes.append(building)

        if building.__class__.__name__ == "Generator":
            self.generators.append(building)

        return building

    def calculate_power(self):
        # Reset power before calculating power again.
        self.power = 0

        for generator in self.generators:
            self.power += generator.produce()