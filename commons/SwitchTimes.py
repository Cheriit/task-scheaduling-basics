from copy import copy
from statistics import mean
from typing import List


class SwitchTimes:
    _switch_times: List[int]
    _mean_time: int

    def __init__(self, times: List[int]):
        self._switch_times = copy(times)
        self._mean_time = mean(times)

    def __str__(self) -> str:
        string_switch_times = map(lambda x: str(x), self._switch_times)
        return (' '.join(string_switch_times)).strip() + '\n'

    def __getitem__(self, item) -> int:
        return self._switch_times[item]

    def __len__(self) -> int:
        return len(self._switch_times)

    def __add__(self, other: int):
        self._switch_times.append(other)

    def get_top_time(self) -> int:
        return self._top_time

    def get_mean_time(self) -> int:
        return self._mean_time
