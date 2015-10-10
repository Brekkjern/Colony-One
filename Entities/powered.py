class Powered(object):
    """Object model for powered structures."""

    def __init__(self, passive, active, powered=False):
        self.passive = passive
        self.active = active
        self.powered = powered