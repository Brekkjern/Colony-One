class Structure(object):
    """Object model for structures."""

    def __init__(self, colony, health=100, max_workers=0):
        self.destroyed = False
        self.health = health
        self.colony = colony
        self.power = {'passive': 0, 'active': 0}
        self.assigned_workers = []
        self.max_workers = max_workers

    def update(self):
        return None

    def damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.destroyed = True

    def add_worker(self, worker):
        if len(self.assigned_workers) >= self.max_workers:
            return False

        self.assigned_workersworkers.append(worker)
        return True

    def is_available_power(self):
        return self.colony['power'] >= self.power['active']

    def produce(self):
        for worker in self.workers:
            if self.is_available_power():
                self.productivity['progress'] += worker.do_work()
                self.colony['power'] -= self.power['active']

    def check_progress(self):
        if self.productivity['progress'] > self.task['goal']:
            self.productivity['progress'] -= self.task['goal']
            return self.task['product']