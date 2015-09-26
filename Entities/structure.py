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
