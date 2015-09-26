class Colonist(object):
    """Object model for colonists."""

    def __init__(self, health=100, age=0, education=None, death_threshold=100):
        self.health = health
        self.dead = False
        self.age = age
        self.education = {'engineering': 0, 'science':0}
        self.deathThreshold = death_threshold

    def update(self):
        pass

    def do_work(self):
        return game_difficulty['morale'] * colony['morale'] * self.health

    def is_worker(self):
        return self.age >= 16

    def is_engineer(self):
        return self.education['engineering'] == 100

    def is_scientist(self):
        return self.education['science'] == 100