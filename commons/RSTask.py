from commons import SwitchTimes, Task


class RSTask(Task):
    deadline_time: int
    switch_times: SwitchTimes

    def __init__(self, ready_time: int, duration_time: int, deadline_time: int):
        super().__init__(duration_time, ready_time)
        self.deadline_time = deadline_time

    def __str__(self) -> str:
        return f'{self.duration_time} {self.ready_time} {self.deadline_time}'.strip() + '\n'
