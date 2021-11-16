from typing import List

from commons import Task


class Machine():
    current_time: float
    tasks: List[Task]
    speedup: int

    def __init__(self, speedup):
        self.speedup = speedup
        self.current_time = 0
        self.tasks = []

    def __str__(self) -> str:
        result = ''
        for task in self.tasks:
            result += f'{task.index} '
        return result.strip() + '\n'

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.current_time = max(self.current_time, task.ready_time) + (task.duration_time / self.speedup)
