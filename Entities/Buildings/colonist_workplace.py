from typing import List

from Entities.Colonists.colonist import Colonist


class ColonistWorkplace(object):

    # Table to hold all references to Colonist_Workplace components.
    colonist_workplaces = []

    def __init__(self, assigned_workers: List[Colonist] = None):
        self.__class__.colonist_workplaces.append(self)

        if assigned_workers:
            self.assigned_workers = assigned_workers
        else:
            self.assigned_workers = []

    def update(self):
        pass

    def tick(self):
        pass

    def work(self, task):
        colonist_work = 0
        for worker in self.assigned_workers:
            colonist_work += worker.do_work(task)

        return colonist_work

    def assign_colonist(self, colonist: Colonist) -> bool:
        if colonist not in self.assigned_workers:
            self.assigned_workers.append(colonist)
            return True
        else:
            return False

    def remove_colonist(self, colonist: Colonist) -> bool:
        self.assigned_workers.remove(Colonist)
        return True
