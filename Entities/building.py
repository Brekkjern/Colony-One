from Entities.structure import Structure


class Building(Structure):
    """Object model for buildings, based on structures."""

    def __init__(self):
        super().__init__()
        self.task = {'goal': 0, 'product': 'Item'}
        self.productivity = {'speed': 1, 'modifier': 0.5, 'progress': 0}

    def update(self):
        return super(Building, self).update()

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
