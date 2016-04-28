import random


class Trait(object):
    """Object model for colonist traits."""

    def __init__(self, name=None, dominant=False, inheritance_chance=0.1, attributes=None, skills=None, active= True):

        if not attributes:
            self.attributes = {}

        if not skills:
            self.skills = {}

        self.name = name
        self.dominant = dominant
        self.chance = inheritance_chance
        self.active = active

    def inherit(self):
        return random.random() < self.chance

    def __eq__(self, other):
        return self.name == other.name
