from typing import List


class FlowTask:
    index: int
    deadline_time: int
    earliness_weight: int
    delay_weight: int
    times: List[int]
    time_sum: int
    late_criterium: float

    def __init__(self, times: List[int], deadline_time: int, earliness_weight: int, delay_weight: int):
        self.deadline_time = deadline_time
        self.earliness_weight = earliness_weight
        self.delay_weight = delay_weight
        self.times = times
        self.time_sum = sum(times)
        self.late_criterium = self.delay_weight / self.time_sum

    def __str__(self) -> str:
        times = " ".join([str(int(x)) for x in self.times])
        return f'{times} {self.deadline_time} {self.earliness_weight} {self.delay_weight}'.strip() + '\n'

    def set_index(self, index: int):
        self.index = index
