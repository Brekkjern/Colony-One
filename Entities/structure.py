class Structure(object):
    """Object model for structures."""

    def __init__(self, requires_power=None, pwr_generator=None,  health=100, max_workers=0):
        self.destroyed = False
        self.health = health
        self.requires_power = requires_power
        self.pwr_generator = pwr_generator
        self.max_workers = max_workers
        self.task = {'goal': 0, 'product': 'Item'}
        self.productivity = {'speed': 1, 'modifier': 0.5, 'progress': 0}

    def update(self):
        self.produce()

    def damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.destroyed = True

    def repair(self, dmg):
        self.health += dmg
        if self.health >= 100:
            self.health = 100

    def produce(self, workers):
        for worker in workers:
            self.productivity['progress'] += worker.do_work()

    def check_progress(self):
        if self.productivity['progress'] > self.task['goal']:
            self.productivity['progress'] -= self.task['goal']
            return self.task['product']

    def needs_power(self):
        return bool(self.powered)
