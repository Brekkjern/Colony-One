import weakref

from Components.powerproperties import PowerGenerator, PowerConsumer
from Entities.colonist import Colonist
from .entity import Entity


class Colony(Entity):
    """Object model for Colony objects"""

    # Table to hold all references to colony entities. Allows for fast listing of all entities.
    colonies = []

    def __init__(self, entity_id, game_settings, colonists = None, buildings = None, stockpile = None):
        super(Colony, self).__init__(entity_id)
        self.__class__.colonies.append(weakref.proxy(self))

        if not colonists:
            colonists = []

        if not buildings:
            buildings = []

        if not stockpile:
            stockpile = []

        self.colonists = colonists
        self.buildings = buildings
        self.agridomes = []
        self.stockpile = stockpile
        self.power_production = 0
        self.power_consumption = 0
        self.power_mod = 0
        self.game_settings = game_settings

    def update(self):
        super(Colony, self).update()

        for building in self.buildings:
            self.add_to_stockpile(building.check_progress())

    def tick(self):
        # Reset all dynamic variables
        self.power_consumption = 0
        self.power_production = 0
        self.agridomes = []

        super(Colony, self).tick()

        # Update the power
        for building in self.buildings:
            if isinstance(building, PowerGenerator):
                self.power_production += building.power_production

            if isinstance(building, PowerConsumer):
                self.power_production += building.power_consumption

        # Update the power production modifier
        self.power_mod = clamp(self.power_production / self.power_consumption, 0, 1)

        # Run the tick on all buildings.
        # As far as I am aware this isn't possible to run in the same loop as
        # the previous loop as we don't know how much power we have available.
        for building in self.buildings:
            building.tick(self.power_mod)

    def add_to_stockpile(self, item):
        self.stockpile.append(item)

    def new_colonist(self) -> Colonist:
        colonist = Colonist(self.game_settings)
        self.colonists.append(colonist)
        return colonist


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)
