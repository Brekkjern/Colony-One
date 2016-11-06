import random
import weakref
from typing import Dict


class Trait(object):
    """Object model for colonist traits."""

    # Table to hold all references to traits. Allows for fast listing of all entities.
    traits = []

    def __init__(self, name: str, dominant: bool, inheritance_chance: float, active: bool,
                 attributes: Dict = None, skills: Dict = None):

        # Appends the new trait to the list of traits
        self.__class__.traits.append(weakref.proxy(self))

        if not attributes:
            attributes = {}

        if not skills:
            skills = {}

        self.attributes = attributes
        self.skills = skills
        self.name = name
        self.dominant = dominant
        self.chance = inheritance_chance
        self.active = active

    def inherit(self) -> bool:
        return random.random() < self.chance

    def get_attribute_modifier(self, attribute: str) -> float:
        if self.active:
            return self.attributes[attribute]
        else:
            return 0
