class Powered(Object):
    """Object model for powered structures."""

    def __init__(self, colony, passive, active, powered=False):
        self.colony = colony
        self.passive = passive
        self.active = active
        self.powered = powered