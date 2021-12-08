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
        times = " ".join([str(x) for x in self.times])
        return f'{times} {self.deadline_time} {self.earliness_weight} {self.delay_weight}'.strip() + '\n'

    def set_index(self, index: int):
        self.index = index

    def set_score(self):
        pass

