class Structure(object):
    """Object model for structures."""

    def __init__(self, powered=None, pwr_generator=None,  health=100, max_workers=0):
        self.destroyed = False
        self.health = health
        self.powered = powered
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
        if self.powered is None:
            return False
        else:
            return True


class PoweredStructure(object):
    """Object model for powered structures."""

    def __init__(self, passive, active, powered=False):
        self.passive = passive
        self.active = active
        self.powered = powered


class Pwr_GeneratorStructure(object):
    """Object model for powered structures."""

    def __init__(self, amount=0, priority=0):
        self.amount = amount
        self.priority = priority