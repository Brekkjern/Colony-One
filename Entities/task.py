class Task(object):
    """Object model for tasks."""

    def __init_(self, skill: str, input=None, output: object = None, progress: float = 0, goal: float = 1):
        self.skill = skill
        self.input = input
        self.output = output
        self.progress = progress
        self.goal = goal
        self.__power_modifier = 0

    @property
    def power_modifier(self) -> float:
        return self.__power_modifier

    @power_modifier.setter
    def power_modifier(self, value: float):
        self.__power_modifier = clamp(value, 0, 1)

    def progress_task(self, amount: float) -> bool:
        if not self.completed():
            self.progress += amount
            return True
        else:
            return False

    def completed(self) -> bool:
        return self.progress >= self.goal

    def return_task_output(self) -> object:
        return self.output


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)
