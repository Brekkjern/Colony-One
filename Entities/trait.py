import random
import weakref


class Trait(object):
    """Object model for colonist traits."""

    # Table to hold all references to traits. Allows for fast listing of all entities.
    traits = []

    def __init__(self, name=None, dominant=False, inheritance_chance=0.1, attributes=None, skills=None, active= True):

        # Appends the new trait to the list of traits
        self.__class__.traits.append(weakref.proxy(self))

        if not attributes:
            self.attributes = {}

        if not skills:
            self.skills = {}

        self.name = name
        self.dominant = dominant
        self.chance = inheritance_chance
        self.active = active

    def inherit(self) -> bool:
        return random.random() < self.chance

    def __eq__(self, other: object) -> bool:
        return self.name == other.name
