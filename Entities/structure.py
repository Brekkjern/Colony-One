import weakref

from Entities.entity import Entity


class Structure(Entity):
    """Object model for structures."""

    # Table to hold all references to structure entities. Allows for fast listing of all entities.
    structures = []

    def __init__(self, entity_id, powered=None, health=100, task=None, input_slot=None, output_slot=None):
        super(Structure, self).__init__(entity_id)
        self.__class__.structures.append(weakref.proxy(self))

        if not input_slot:
            input_slot = []

        if not output_slot:
            output_slot = []

        self.destroyed = False
        self.health = health
        self.powered = powered
        self.task = task
        self.input_slot = input_slot
        self.output_slot = output_slot

    def update(self):
        super(Structure, self).update()
        if self.health > 0:
            self.alive = False

        self.output_slot.append(self.check_progress())

    def tick(self):
        super(Structure, self).tick()

    def damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.destroyed = True

    def repair(self, dmg):
        self.health += dmg
        if self.health >= 100:
            self.health = 100

    def work(self, work):
        self.task.perform_task(work)

    def check_progress(self):
        if self.task.check_progress():
            output = self.task.return_output()
            self.task = None
            return output
        else:
            return None

    def needs_power(self):
        if self.powered is None:
            return False
        else:
            return True
