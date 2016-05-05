import math
import conf
import weakref
from Entities.entity import Entity


class Colonist(Entity):
    """Object model for colonists."""

    # Table to hold all references to colonist entities. Allows for fast listing of all entities.
    colonists = []

    def __init__(self, entity_id, morale=100, health=100, age=0, education=None, hunger=0):
        super(Colonist, self).__init__(entity_id)
        self.__class__.colonists.append(weakref.proxy(self))

        if not education:
            education = {'engineering': 0, 'science': 0}

        self.education = education
        self.morale = morale
        self.health = health
        self.age = age
        self.hunger = hunger

        # Stats
        self.attributes = {
            'wisdom': 10,
            'logic': 10,
            'focus': 10,
            'endurance': 10,
            'dexterity': 10
        }

        self.skills = {

        }

        # Traits
        self.traits = []

    def update(self):
        super(Colonist, self).update()
        if self.health > 0:
            self.alive = False

    def tick(self):
        super(Colonist, self).tick()
        # Add a day to the colonist age.
        self.age += 1

        # Reduce hunger.
        self.hunger -= 1

        if self.age < self.life_expectancy():
            self.alive = False

        if not self.alive:
            print("DEBUG: Colonist {} died on tick {}.".format(self.entity_id, conf.tick))

    def apply_trait_effect(self, trait: object) -> bool:
        if trait.active:
            for attribute, modifier in trait.attributes.items():
                self.attributes[attribute] += modifier

            for skill, modifier in trait.skills.items():
                self.skills[skill] += modifier
            return True
        return False

    def assign_trait(self, new_trait: object) -> bool:
        if new_trait not in self.traits:
            self.traits.append(new_trait)
            self.apply_trait_effect(new_trait)
            return True
        return False

    def change_health(self, target: float, divider: float) -> float:
        return (target - self.health) / divider

    def life_expectancy(self) -> float:
        # Years / (1 + 10^(-0.1 * health))
        return 80 * conf.game_settings['ticks_per_year'] / (1 + math.exp(-0.1 * self.health))

    def fertility(self) -> float:
        # This is a standard parabolic function expressed as y = a (x - h)^2 + (bx) + k
        # "a" determines the slope of the graph
        # "h" determines the point where the graph turns
        # "k" determines the lowest number "y" can be
        # "b" moves the bottom point of the parabola in a reverse parabolic arc
        # y = 0.25(x-35)^2+(-0.3x)+20

        age = self.age / conf.game_settings['ticks_per_year']
        return (0.25 * (age - 35) ** 2) + (-0.3 * age) + 15

    def do_work(self, building: object) -> float:
        morale = conf.game_settings['morale'] * self.morale
        attributes = self.attributes[building.task.attributes[0]] * (self.attributes[building.task.attributes[1]] / 2)
        return morale * self.health * attributes
