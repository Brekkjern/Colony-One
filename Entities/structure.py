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
