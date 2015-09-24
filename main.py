# Global variables for the colony
colony = {
    'power': 50, 'morale': 50, 'food': 50, }

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
    health = 100

    def update(self):
        pass

    def damage(self, dmg):
        self.health -= dmg

        if self.health <= 0:
            pass


class Building(Structure):
    power = {
        'passive': 0, 'active': 0
    }

    workers = {
        'max': 0, 'assigned': 0
    }

    task = {
        'goal': 0, 'product': "Item"
    }

    productivity = {
        'speed': 1, 'modifier': 0.5, 'progress': 0
    }

    def update(self):
        return super(Building, self).update()

    def do_work(self):
        for i in range(0, self.workers["assigned"]+1):
            if colony['power'] >= self.power['active']:
                self.productivity['progress'] += self.productivity['speed'] * self.productivity['modifier'] * colony[
                    'morale'] / 100
                colony['power'] -= self.power['active']

    def check_progress(self):
        if self.productivity['progress'] > self.task['goal']:
            self.productivity['progress'] -= self.task['goal']
            return self.task['product']
