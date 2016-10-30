import weakref


class Entity(object):
    # Table to hold all references of entities. Allows for fast listing of all entities.
    entities = []

    def __init__(self, entity_id: int):
        self.__class__.entities.append(weakref.proxy(self))
        self.entity_id = entity_id
        self.alive = True

    def update(self, *args):
        pass

    def tick(self, *args):
        pass
