class PowerGenerator(object):

    power_generators = []

    def __init__(self, power_production: float):
        self.__class__.power_generators.append(self)
        self.power_production = power_production
        self.idle = False

    def update(self):
        pass

    def tick(self, status):
        pass


class PowerConsumer(object):

    power_consumers = []

    def __init__(self, power_consumption: float, idle_threshold: float):
        self.__class__.power_consumers.append(self)
        self.power_consumption = power_consumption
        self.idle_threshold = idle_threshold
        self.idle = False

    def update(self):
        pass

    def tick(self, status, power_modifier):
        self.idle = power_modifier < self.idle_threshold
