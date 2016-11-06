class PowerGenerator(object):
    def __init__(self, power_production: float):
        self.power_production = power_production
        self.idle = False

    def update(self):
        pass

    def tick(self, status):
        pass


class PowerConsumer(object):
    def __init__(self, power_consumption: float, idle_threshold: float):
        self.power_consumption = power_consumption
        self.idle_threshold = idle_threshold
        self.idle = False

    def update(self):
        pass

    def tick(self, status, power_modifier):
        self.idle = power_modifier < self.idle_threshold
