from Entities.structure import Structure
from Entities.colonist import Colonist

class Colony(object):
    """Object model for Colony objects"""

    def __init__(self, colonists = None):
        if not colonists:
            self.colonists = []

        self.colonists = colonists
        self.power = 0
        self.food = 0

    def update(self):
        for colonist in self.colonists:
            colonist.update()