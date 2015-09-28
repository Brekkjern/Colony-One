class Structure(object):
    """Object model for structures."""

    def __init__(self, colony, health=100, max_workers=0):
        self.destroyed = False
        self.health = health
        self.colony = colony
        self.power = {'passive': 0, 'active': 0}
        self.assigned_workers = []
        self.max_workers = max_workers
        self.task = {'goal': 0, 'product': 'Item'}
        self.productivity = {'speed': 1, 'modifier': 0.5, 'progress': 0}

    def update(self):
        self.produce()

    def damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.destroyed = True

    def add_worker(self, worker):
        if len(self.assigned_workers) >= self.max_workers:
            return False

        self.assigned_workers.append(worker)
        return True

    def produce(self):
        for worker in self.assigned_workers:
            if self.colony.is_available_power(self.power['active']):
                self.productivity['progress'] += worker.do_work()
                self.colony['power'] -= self.power['active']

    def check_progress(self):
        if self.productivity['progress'] > self.task['goal']:
            self.productivity['progress'] -= self.task['goal']
            return self.task['product']

