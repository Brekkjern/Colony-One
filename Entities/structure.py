class Structure(object):
    """Object model for structures."""

    def __init__(self, colony, powered=None, health=100, max_workers=0):
        self.destroyed = False
        self.health = health
        self.colony = colony
        self.powered = powered
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

    def repair(self, dmg):
        self.health += dmg
        if self.health >= 100:
            self.health = 100

    def add_worker(self, worker):
        # Add a worker to the building. Requires a worker object.
        if len(self.assigned_workers) >= self.max_workers:
            return False

        self.assigned_workers.append(worker)
        return True

    def produce(self):
        for worker in self.assigned_workers:
            if self.colony.request_power(self.powered.active):
                self.productivity['progress'] += worker.do_work()

    def check_progress(self):
        if self.productivity['progress'] > self.task['goal']:
            self.productivity['progress'] -= self.task['goal']
            return self.task['product']

    def needs_power(self):
        return bool(self.powered)
