class Task(object):
    """Object model for tasks."""

    def __init_(self, input=None, output=None, progress=0, goal=1 ):
        self.input = input
        self.output = output
        self.progress = progress
        self.goal = goal

    def perform_task(self, amount: float) -> float:
        self.progress += amount
        return self.progress

    def check_progress(self) -> bool:
        return self.progress >= self.goal

    def return_output(self) -> object:
        return self.output