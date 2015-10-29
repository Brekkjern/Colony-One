from Entities.structure import Structure
from Entities.colonist import Colonist

class Colony(object):
    """Object model for Colony objects"""

    def __init__(self, game_settings, colonists=None, buildings=None):
        if not colonists:
            colonists = []

        if not buildings:
            buildings = []

        self.colonists = colonists
        self.buildings = buildings
        self.power = 0
        self.food = 0
        self.game_settings = game_settings

    def update(self, tick):
        alive_colonists = []
        for colonist in self.colonists:
            colonist.update(tick)

            if not colonist.dead:
                alive_colonists.append(colonist)

        for building in self.buildings:
            building.update()

        self.colonists = alive_colonists

    def request_power(self, power):
        # Drain a select amount of power from the colony if it's available.
        if self.power >= power:
            self.power -= power
            return True

        return False

    def new_colonist(self):
        self.colonists.append(Colonist(self.game_settings))