class Colonist(object):
    """Object model for colonists."""

    def __init__(self, health=100, age=0, education=None, death_threshold=100):
        self.health = health
        self.dead = False
        self.age = age
        self.education = education
        self.deathThreshold = death_threshold

    def update(self):
        pass

    def do_work(self):
        return game_difficulty['morale'] * colony['morale'] * self.health