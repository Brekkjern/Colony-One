import random


class Trait(object):
    """Object model for colonist traits."""

    def __init__(self, name=None, dominant=False, inheritance_chance=0.1, abilities=None, skills=None):

        if not abilities:
            self.abilities = {}

        if not skills:
            self.skills = {}

        self.name = name
        self.recessive = dominant
        self.chance = inheritance_chance

    def inherit(self):
        return random.random() < self.chance

    def __eq__(self, other):
        return self.name == other.name
