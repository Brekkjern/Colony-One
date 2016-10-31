import weakref

from Entities.entity import Entity
from Entities.hexmap import Axial


class WorldEntity(Entity):
    # Table to hold all references of world entities. Allows for fast listing of all entities.
    world_entities = []

    def __init__(self, entity_id: int, location: Axial):
        super(WorldEntity, self).__init__(entity_id)
        self.__class__.world_entities.append(weakref.proxy(self))
        self.location = location

    def update(self, *args):
        super(WorldEntity, self).update(*args)

    def tick(self, *args):
        super(WorldEntity, self).tick(*args)
