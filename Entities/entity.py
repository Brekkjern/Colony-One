from Entities.entity_master import Entity_Master

class Entity(Object):
    def __init__(self):
        self.entity_id = Entity_Master.get_next_entity_id()