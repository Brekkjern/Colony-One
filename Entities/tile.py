import Entities.entity
from Components.renderer import Renderer
from Systems.hexmap import Axial


class Tile(Entities.entity.Entity):
    def __init__(self, entity_id, location: Axial, rendering_component: Renderer):
        super(Tile, self).__init__(entity_id)
        self.location = location
        self.renderer = rendering_component

