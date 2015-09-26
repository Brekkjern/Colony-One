class Colonist(object):
    """Object model for colonists."""

    def __init__(self, game_settings, morale = 100, health = 100, age = 0, death_threshold = 100,
                 education = {'engineering': 0, 'science': 0}):
        self.game_settings = game_settings
        self.morale = morale
        self.health = health
        self.dead = False
        self.age = age
        self.education = education
        self.deathThreshold = death_threshold

    def update(self):
        # Add a day to the colonist age.
        self.age += 1

    def do_work(self):
        return self.game_settings['morale'] * self.morale * self.health

    def is_worker(self):
        return self.age >= (16 * self.game_settings['time']['year'])

    def is_engineer(self):
        return self.education['engineering'] == 100

    def is_scientist(self):
        return self.education['science'] == 100
