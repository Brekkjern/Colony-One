import math


class Colonist(object):
    """Object model for colonists."""

    def __init__(self, game_settings, morale = 100, health = 100, age = 0, education = None):
        if not education:
            education = {'engineering': 0, 'science': 0}

        self.education = education
        self.game_settings = game_settings
        self.morale = morale
        self.health = health
        self.dead = False
        self.age = age

    def update(self):
        # Add a day to the colonist age.
        self.age += 1

        # Check to see if colonist is older than life expectancy.
        self.dead = self.age >= self.life_expectancy()

    def life_expectancy(self):
        return (80 * self.game_settings['year']) / (1 + math.e() ** (-0.1 * self.health))

    def fertility(self):
        # This is a standard parabolic function expressed as y = a (x - h)^2 + (bx) + k
        # "a" determines the slope of the graph
        # "h" determines the point where the graph turns
        # "k" determines the lowest number "y" can be
        # "b" moves the bottom point of the parabola in a reverse parabolic arc
        # y = 0.25(x-35)^2+(-0.3x)+20

        age = self.age / self.game_settings['year']
        return (0.25(age - 35) ** 2) + (-0.3 * age) + 15

    def do_work(self):
        return self.game_settings['morale'] * self.morale * self.health

    def is_worker(self):
        return self.age >= (16 * self.game_settings['time']['year'])

    def is_engineer(self):
        return self.education['engineering'] == 100

    def is_scientist(self):
        return self.education['science'] == 100
