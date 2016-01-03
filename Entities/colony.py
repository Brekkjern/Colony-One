from Entities.structure import Structure
from Entities.colonist import Colonist
import conf


class Colony(object):
    """Object model for Colony objects"""

    def __init__(self, game_settings, colonists=None, buildings=None):
        if not colonists:
            colonists = []

        if not buildings:
            buildings = []

        self.colonists = colonists
        self.buildings = buildings
        self.power_generators = []
        self.power = 0
        self.food = 0
        self.game_settings = game_settings

    def update(self):

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

    def new_building(self):
        building = Structure()
        self.buildings.append(building)

        if building.pwr_generator:
            self.power_generators.append(building)

        return building