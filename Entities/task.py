class Task(object):
    """Object model for tasks."""

    def __init_(self, skill: str, input = None, output: object = None, progress: float = 0, goal: float = 1):
        self.skill = skill
        self.input = input
        self.output = output
        self.progress = progress
        self.goal = goal

    def progress_task(self, amount: float) -> bool:
        if not self.is_completed():
            self.progress += amount
            return True
        else:
            return False

    def is_completed(self) -> bool:
        return self.progress >= self.goal

    def return_task_output(self) -> object:
        return self.output