# The state of the colony
colony = {
    'power': 50, 'morale': 50, 'food': 50, }

# The state of the population
population = {
    'children': 0,
    'workers': {
        'assigned': 0,
        'total': 0
    },
    'scientists': {
        'assigned': 0,
        'total': 0
    }
}


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

    def __init__(self):
        self.power = {'passive': 0, 'active': 0}
        self.workers = {'max': 0, 'assigned': 0}
        self.task = {'goal': 0, 'product': 'Item'}
        self.productivity = {'speed': 1, 'modifier': 0.5, 'progress': 0}

    def update(self):
        return super(Building, self).update()

    def do_work(self):
        for count in range(self.workers['assigned']):
            if colony['power'] >= self.power['active']:
                self.productivity['progress'] += self.productivity['speed'] * self.productivity['modifier'] * colony[
                    'morale'] / 100
                colony['power'] -= self.power['active']

    def check_progress(self):
        if self.productivity['progress'] > self.task['goal']:
            self.productivity['progress'] -= self.task['goal']
            return self.task['product']
