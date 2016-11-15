import Components.renderer as renderer
import Systems.hexmap as hexmap


class Tile(object):
    def __init__(self, position: hexmap.Axial, rendering_component: renderer.Renderer):
        self.position = position
        self.renderer = rendering_component
