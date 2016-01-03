class Structure(object):
    """Object model for structures."""

    def __init__(self, powered=None, pwr_generator=None, health=100, workers=None):
        if not workers:
            workers = {'minimum': 0, 'maximum': 0}

        self.destroyed = False
        self.health = health
        self.powered = powered
        self.pwr_generator = pwr_generator
        self.workers = workers
        self.task = {'goal': 0, 'product': 'Item'}
        self.productivity = {'speed': 1, 'modifier': 0.5, 'progress': 0}

    def update(self):
        self.work()

    def damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.destroyed = True

    def repair(self, dmg):
        self.health += dmg
        if self.health >= 100:
            self.health = 100

    def work(self, workers):
        for worker in workers:
            self.productivity['progress'] += worker.do_work()

    def check_progress(self):
        if self.productivity['progress'] > self.task['goal']:
            self.productivity['progress'] -= self.task['goal']
            self.produce()

    def needs_power(self):
        if self.powered is None:
            return False
        else:
            return True


class PoweredStructure(object):
    """Object model for powered structures. Used in composition together with Structure class."""

    def __init__(self, passive, active, powered=False):
        self.passive = passive
        self.active = active
        self.powered = powered


class Pwr_GeneratorStructure(object):
    """Object model for powered structures. Used in composition together with Structure class."""

    def __init__(self, amount=0, priority=0):
        self.amount = amount
        self.priority = priority

class Agridome(Structure):
    """Object model for food producing structure. Child class of Structure."""

    def __init__(self, capacity=0, production_modifier=1):
        super(Agridome, self).__init__()
        self.capacity = capacity
        self.production_modifier = production_modifier

    def produce(self):
        self.capacity += 1 * self.production_modifier