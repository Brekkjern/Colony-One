class Task(object):
    """Object model for tasks."""

    def __init_(self, input=None, output=None, progress=0, goal=1 ):
        self.input = input
        self.output = output
        self.progress = progress
        self.goal = goal

    def perform_task(self, amount):
        self.progress += amount

    def check_progress(self):
        return self.progress >= self.goal

    def return_output(self):
        return self.output