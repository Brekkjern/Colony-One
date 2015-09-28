from Entities.structure import Structure
from Entities.colonist import Colonist

class Colony(object):
    """Object model for Colony objects"""

    def __init__(self, colonists=None, buildings=None):
        if not colonists:
           colonists = []

        if not buildings:
            buildings = []

        self.colonists = colonists
        self.buildings = buildings
        self.power = 0
        self.food = 0

    def update(self):
        for colonist in self.colonists:
            colonist.update()

        for building in self.buildings:
            building.update()