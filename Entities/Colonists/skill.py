class Skill(object):
    def __init__(self, primary, secondary, level, multiplier):
        self.primary = primary
        self.secondary = secondary
        self.level = level
        self.level_multiplier = multiplier

    def perform_skill(self):
        return (self.primary + (self.secondary / 2)) * (self.level_multiplier * self.level)
