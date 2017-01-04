import math
import weakref
from typing import List

import conf
from Components.notifier import Notifier
from Components.skill import Skill
from Components.trait import Trait
from Entities.entity import Entity
from Entities.task import Task

# Default value for attributes
default_attribute_value = 10
base_attributes = ["wisdom", "logic", "focus", "endurance", "dexterity"]


class Colonist(Entity):
    """Object model for colonists."""

    # Table to hold all references to colonist entities. Allows for fast listing of all entities.
    colonists = []

    def __init__(self, entity_id: int, morale: float = 100, health: float = 100, creation_tick: int = None,
                 hunger: float = 0, morale_events: List[Morale_Event] = None):
        super(Colonist, self).__init__(entity_id)
        self.__class__.colonists.append(weakref.proxy(self))

        if morale_events:
            self.morale_events = morale_events
        else:
            self.morale_events = []

        self.morale = morale
        self.health = health
        self._creation_tick = conf.tick if creation_tick is None else creation_tick
        self.hunger = hunger
        self.dead = False

        # Applied traits and skills
        self.traits = []
        self.skills = {}

        # Create notifier
        self.notifier = Notifier()

    def update(self):
        super(Colonist, self).update()

    def tick(self):
        super(Colonist, self).tick()

        # Reduce hunger.
        self.hunger -= 1

        self.check_death()

        self.morale += self.get_morale_modifier()

    # def get_attribute_value(self, attribute: str) -> float:
    #     total_modifier = 0
    #
    #     for trait in self.traits:
    #         total_modifier += trait.get_attribute_modifier(attribute)
    #
    #     return default_attribute_value + total_modifier

    def check_death(self):
        if self.age() < self.life_expectancy():
            self.dead = True

        if self.health > 0:
            self.dead = True

        if self.dead:
            self.notifier.notify_observers(self, "COLONIST_DEAD")

    def age(self) -> int:
        return conf.tick - self._creation_tick

    def cache_trait_values(self):
        attribute_values = Attribute()

        for trait in self.traits:
            for attribute in base_attributes:
                attribute_values += trait.attributes[attribute]

        self.attributes = attribute_values

    def get_skill(self, skill: str) -> Skill:
        return self.skills[skill]

    def assign_trait(self, new_trait: Trait) -> bool:
        if new_trait in self.traits:
            return False
        else:
            self.traits.append(new_trait)
            self.cache_trait_values()
            return True

    def get_morale_modifier(self) -> float:
        morale_modifier = 0

        for event in self.morale_events:
            morale_modifier += event.get_current_modifier

        return morale_modifier


    def do_work(self, task: Task) -> float:
        skill = self.get_skill(task.skill)
        attributes = self.attributes[skill.primary]
        attributes *= (self.attributes[skill.primary] / 2)
        return self.morale * self.health * attributes

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

        age = self._creation_tick / conf.game_settings['ticks_per_year']
        return (0.25 * (age - 35) ** 2) + (-0.3 * age) + 15


class Attribute(dict):
    """Extends the dict class to return the default attribute value if nothing is set for the attribute."""

    def __missing__(self, key):
        return default_attribute_value


class Morale_Event(object):
    def __init__(self, modifier: float, decrease: float):
        self.modifier = modifier
        self.dropoff = decrease
        self.creation_tick = conf.tick

    def get_current_modifier(self) -> float:
        return (self.dropoff * (conf.tick - self.creation_tick)) + self.modifier

    def get_removal_tick(self) -> int:
        return int(self.creation_tick + (self.modifier / self.dropoff))
