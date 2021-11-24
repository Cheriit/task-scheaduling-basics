from commons import Task


class RWTask(Task):
    deadline_time: int
    priority: int
    score: float

    def __init__(self, ready_time: int, duration_time: int, deadline_time: int, priority: int):
        super().__init__(duration_time, ready_time)
        self.deadline_time = deadline_time
        self.priority = priority

    def __str__(self) -> str:
        return f'{self.duration_time} {self.ready_time} {self.deadline_time} {self.priority}'.strip() + '\n'
