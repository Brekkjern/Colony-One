import random
import conf


class Trait(object):
    """Object model for colonist traits."""

    def __init__(self, name=None, recessive=False, inheritance_chance=0.1, stats=None, skills=None):

        if not stats:
            self.stats = {}

        if not skills:
            self.skills = {}

        self.name=name
        self.recessive=recessive
        self.chance=inheritance_chance

    def inherit(self):
        return random.random() < self.chance

    