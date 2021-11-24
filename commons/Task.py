class Task:
    duration_time: float
    index: int
    ready_time: int

    def __init__(self, duration_time: int, ready_time: int):
        self.duration_time = duration_time
        self.ready_time = ready_time

    def set_index(self, index: int):
        self.index = index

    def __str__(self) -> str:
        return f'{self.duration_time} {self.ready_time} \n'
