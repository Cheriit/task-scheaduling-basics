class Task:
    duration_time: int

    def __init__(self, duration_time: int):
        self.duration_time = duration_time

    def __str__(self) -> str:
        return f'{self.duration_time} \n'
