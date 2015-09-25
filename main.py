# Game difficulty modifiers
game_difficulty = {'morale': 0.5}

# The state of the colony
colony = {
    'power': 50, 'morale': 50, 'food': 50, }

# List of population
population = []


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


class Structure(object):
    """Object model for structures."""

    def __init__(self, health=100):
        self.destroyed = False
        self.health = health

    def update(self):
        return None

    def damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.destroyed = True


class Building(Structure):
    """Object model for buildings, based on structures."""

    def __init__(self, max_workers=0):
        super().__init__()
        self.power = {'passive': 0, 'active': 0}
        self.workers = []
        self.max_workers = max_workers
        self.task = {'goal': 0, 'product': 'Item'}
        self.productivity = {'speed': 1, 'modifier': 0.5, 'progress': 0}

    def update(self):
        return super(Building, self).update()

    def add_worker(self, worker):
        if len(self.workers) >= self.max_workers:
            return False

        self.workers.append(worker)
        return True

    def is_available_power(self):
        return colony['power'] >= self.power['active']

    def produce(self):
        for worker in self.workers:
            if self.is_available_power():
                self.productivity['progress'] += worker.do_work()
                colony['power'] -= self.power['active']

    def check_progress(self):
        if self.productivity['progress'] > self.task['goal']:
            self.productivity['progress'] -= self.task['goal']
            return self.task['product']


