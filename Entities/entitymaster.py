from Entities.structure import Structure
from Entities.colonist import Colonist
from Entities.entity import Entity


class EntityMaster(object):
    def __init__(self, last_entity_id = 0, entities = None, member_list = None):

        if not entities:
            entities = {}

        if not member_list:
            member_list = {}

        self.last_entity_id = last_entity_id

        # Entity list contains a list of entity objects
        self.entities = entities

        # Member list contains a list of lists of the structure [colony, entity]
        self.member_list = member_list

    def tick(self):
        for entity in sorted(self.entities, reverse = True):
            entity.tick()

    def update(self):
        for entity_id, entity in sorted(self.entities, reverse=True):
            entity.update()

            if not entity.alive:
                self.remove_entity_from_colony(entity.entity_id)
                del self.entities[entity_id]

    def get_new_entity_id(self) -> int:
        self.last_entity_id += 1
        return self.last_entity_id

    def get_entity(self, entity_id: int) -> Entity:
        return self.entities[entity_id]

    def get_colony_entity_list(self, colony_id: int) -> list:
        members = []

        for colonist, colony in self.member_list:
            if colony == colony_id:
                members.append(colonist)

        return members

    def add_entity_to_colony(self, entity_id: int, colony: int):
        if self.get_entity_colony(entity_id):
            self.remove_entity_from_colony(entity_id)

        self.member_list[entity_id] = colony

    def remove_entity_from_colony(self, entity_id: int) -> bool:
        del self.member_list[entity_id]

    def get_entity_colony(self, entity_id: int) -> int:
        return self.member_list[entity_id]

    def add_entity(self, entity: Entity):
        self.entities[entity.entity_id] = entity

    def new_colonist(self, colony_id: int) -> Colonist:
        colonist = Colonist(self.get_new_entity_id())
        self.add_entity(colonist)
        self.add_entity_to_colony(colonist.entity_id, colony_id)
        return colonist
