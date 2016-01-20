import math
import conf


class Colonist(object):
    """Object model for colonists."""

    def __init__(self, morale = 100, health = 100, age = 0, education = None, hunger = 0):
        if not education:
            education = {'engineering': 0, 'science': 0}

        self.education = education
        self.morale = morale
        self.health = health
        self.dead = False
        self.age = age
        self.hunger = hunger

        # Stats
        self.abilities = {
            'wisdom': 10,
            'logic': 10,
            'focus': 10,
            'endurance': 10,
            'dexterity': 10
        }

        # Traits
        self.traits = []



    def update(self):
        # Check to see if colonist is older than life expectancy.
        self.dead = self.age >= self.life_expectancy()
        if self.dead:
            print("DEBUG: Colonist died on tick {}.".format(conf.tick))

    def tick(self):
        # Add a day to the colonist age.
        self.age += 1

        # Reduce hunger.
        self.hunger -= 1

    # Example dict for traits:
    #test_trait = {
    #    'name': "TraitName",
    #    'stats':{'wisdom': -2, 'logic': -2, 'endurance': 2}
    #}

    def assign_trait(self, new_trait):
        for existing_trait in self.traits:
            if new_trait['name'] == existing_trait['name']:
                return False

        for ability, value in new_trait['stats'].items():
            self.abilities[ability] += value
        self.traits.append(new_trait)
        return True

    def change_health(self, target, divider):
        return (target - self.health) / divider

    def life_expectancy(self):
        return 80 * conf.game_settings['ticks_per_year'] / (1 + math.exp(-0.1 * self.health))

    def fertility(self):
        # This is a standard parabolic function expressed as y = a (x - h)^2 + (bx) + k
        # "a" determines the slope of the graph
        # "h" determines the point where the graph turns
        # "k" determines the lowest number "y" can be
        # "b" moves the bottom point of the parabola in a reverse parabolic arc
        # y = 0.25(x-35)^2+(-0.3x)+20

        age = self.age / conf.game_settings['ticks_per_year']
        return (0.25 * (age - 35) ** 2) + (-0.3 * age) + 15

    def do_work(self):
        return conf.game_settings['morale'] * self.morale * self.health

    def is_worker(self):
        return self.age >= (16 * conf.game_settings['ticks_per_year'])

    def is_engineer(self):
        return self.education['engineering'] == 100

    def is_scientist(self):
        return self.education['science'] == 100
