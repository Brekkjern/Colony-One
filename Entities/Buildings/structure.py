import weakref

from Entities.hexmap import Axial
from Entities.worldentity import WorldEntity


class Structure(WorldEntity):
    """Object model for structures."""

    # Table to hold all references to structure entities. Allows for fast listing of all entities.
    structures = []

    def __init__(self, entity_id, location: Axial, health = 100, max_health = 100, task = None, input_slot = None,
                 output_slot = None):
        super(Structure, self).__init__(entity_id, location)
        self.__class__.structures.append(weakref.proxy(self))

        if not input_slot:
            input_slot = []

        if not output_slot:
            output_slot = []

        self.destroyed = False
        self.__health = health
        self.max_health = max_health
        self.task = task
        self.input_slot = input_slot
        self.output_slot = output_slot

    def update(self) -> None:
        super(Structure, self).update()

        self.output_slot.append(self.check_progress())

    def tick(self, power_mod, *args) -> None:
        super(Structure, self).tick()
        self.task.power_modifier = power_mod

        # TODO: Add working task here. Possibly add composition for colonist workplaces?

    @property
    def __health(self) -> float:
        return self.__health

    @__health.setter
    def __health(self, value: float) -> None:
        if not self.destroyed:
            self.__health = clamp(value, 0, self.max_health)

        if self.__health <= 0:
            self.destroyed = True

    def damage(self, dmg):
        self.__health -= dmg

    def repair(self, dmg):
        self.__health += dmg

    def work(self, work):
        self.task.perform_task(work)

    def check_progress(self):
        if self.task.check_progress():
            output = self.task.return_output()
            self.task = None
            return output
        else:
            return None


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)
