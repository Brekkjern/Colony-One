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
        for entity in self.entities:
            if entity.entity_id == entity_id:
                return entity

    def add_entity_to_colony(self, entity: object, colony: int) -> bool:
        if self.get_entity_colony(entity):
            self.remove_entity_from_colony(entity)

        self.member_list.append([colony, entity.entity_id])

    def remove_entity_from_colony(self, entity_id: int) -> bool:
        for entry in self.member_list:
            for colony, entity in entry:
                if entity == entity_id:
                    return self.member_list.remove(entry)

    def get_entity_colony(self, entity_id: int) -> int:
        for entry in self.member_list:
            for colony, entity in entry:
                if entity == entity_id:
                    return colony

    def add_entity(self, entity: object) -> bool:
        return self.entities.append(entity)

    def new_colonist(self, colony: int) -> object:
        colonist = Colonist(self.next_entity_id())
        self.add_entity(colonist)
        self.add_entity_to_colony(colony)
        return colonist