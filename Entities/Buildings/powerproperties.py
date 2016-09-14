class PowerGenerator(object):
    def __init__(self, power_production: float):
        self.power_production = power_production

    def update(self):
        pass

    def tick(self):
        pass


class PowerConsumer(object):
    def __init__(self, power_consumption: float):
        self.power_consumption = power_consumption

    def update(self):
        pass

    def tick(self):
        pass
