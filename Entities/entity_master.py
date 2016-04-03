from Entities.structure import Structure
from Entities.colonist import Colonist

class Entity_Master(object):

    def __init__(self, last_entity_id=0, entities=None,  member_list=None):

        if not entities:
            entities = []

        if not member_list:
            member_list = []

        self.entities = entities
        self.last_entity_id = last_entity_id
        self.member_list = member_list

    def next_entity_id(self) -> int:
        self.last_entity_id += 1
        return self.last_entity_id

    def get_entity(self, entity_id: int) -> object:
        for i, entity in enumerate(self.entities):
            if entity.entity_id == entity_id:
                return entity

    def add_entity_to_colony(self, colonist: object, colony: int) -> bool:
        if self.get_entity_colony(colonist):
            return False
        else:
            self.member_list.append([colony, colonist.entity_id])
            return True

    def remove_entity_from_colony(self, colonist: object) -> bool:
        colony = self.get_entity_colony(colonist)
        if colony:
            self.colonies[colony].remove(colonist)
            return True
        else:
            return False

    def get_entity_colony(self, colonist: object) -> int:
        for colony in self.colony_member_list:
            if colonist in colony:
                return colony

    def add_entity(self, entity: object) -> bool:
        return self.entities.append(entity)

    def new_colonist(self, colony: int) -> object:
        colonist = Colonist(self.next_entity_id())
        self.add_entity(colonist)
        self.add_entity_to_colony(colony)
        return colonist