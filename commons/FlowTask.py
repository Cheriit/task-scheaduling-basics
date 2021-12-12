from typing import List


class FlowTask:
    index: int
    deadline_time: int
    earliness_weight: int
    delay_weight: int
    score: float
    times: List[int]

    def __init__(self, times: List[int], deadline_time: int, earliness_weight: int, delay_weight: int):
        self.deadline_time = deadline_time
        self.earliness_weight = earliness_weight
        self.delay_weight = delay_weight
        self.times = times

    def __str__(self) -> str:
        times = " ".join([str(int(x)) for x in self.times])
        return f'{times} {self.deadline_time} {self.earliness_weight} {self.delay_weight}'.strip() + '\n'

    def set_index(self, index: int):
        self.index = index

    def calculate_score(self, machine_weights, time_weight: float, due_time_param: float, delay_param: float, earliness_param: float):
        self.score = 0
        for i in range(len(self.times)):
            self.score += time_weight * machine_weights[i] * self.times[i]
        self.score += due_time_param * self.deadline_time - delay_param * self.delay_weight - earliness_param * self.earliness_weight
