import common
from Entities.colony import Colony
from Entities.task import Task
from Entities.worldentity import WorldEntity
from Systems.hexmap import Axial


class Structure(WorldEntity):
    """Object model for structures."""

    def __init__(self, entity_id, colony: Colony, location: Axial, health = 100, max_health = 100, task: Task = None,
                 input_slot = None,
                 output_slot = None):
        super(Structure, self).__init__(entity_id, location)

        if not input_slot:
            input_slot = []

        if not output_slot:
            output_slot = []

        self.colony = colony
        self.destroyed = False
        self.__health = health
        self.max_health = max_health
        self.task = task
        self.input_slot = input_slot
        self.output_slot = output_slot

    def update(self) -> None:
        super(Structure, self).update()

        self.output_slot.append(self.check_progress())

    def tick(self, *args) -> None:
        super(Structure, self).tick()

        # TODO: Add working task here. Possibly add composition for colonist workplaces?

    @property
    def __health(self) -> float:
        return self.__health

    @__health.setter
    def __health(self, value: float) -> None:
        if not self.destroyed:
            self.__health = common.clamp(value, 0, self.max_health)

        if self.__health <= 0:
            self.destroyed = True

    def damage(self, dmg):
        self.__health -= dmg

    def repair(self, dmg):
        self.__health += dmg

    def work(self, work):
        self.task.progress_task(work)

    def check_progress(self):
        if self.task.check_progress():
            output = self.task.return_output()
            self.task = None
            return output
        else:
            return None


