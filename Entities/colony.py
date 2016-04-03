from Entities.structure import Structure
from Entities.colonist import Colonist
from Entities.entity import Entity
import conf


class Colony(Entity):
    """Object model for Colony objects"""

    def __init__(self, game_settings, colonists=None, buildings=None, agridomes=None, generators=None, stockpile=None):
        super(Colony, self).__init__()
        if not colonists:
            colonists = []

        if not buildings:
            buildings = []

        if not agridomes:
            agridomes = []

        if not generators:
            generators = []

        if not stockpile:
            stockpile = []

        self.colonists = colonists
        self.buildings = buildings
        self.agridomes = agridomes
        self.generators = generators
        self.stockpile = stockpile
        self.power = 0
        self.food = 0
        self.game_settings = game_settings

    def update(self):

        # Calculate what power is available
        self.calculate_power()

        for building in self.buildings:
            self.add_to_stockpile(building.check_progress())

    def add_to_stockpile(self, item):
            self.stockpile.append(item)

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