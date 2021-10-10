from copy import copy
from typing import List


class SwitchTimes:
    _switch_times: List[int]

    def __init__(self, times: List[int]):
        self._switch_times = copy(times)

    def __str__(self) -> str:
        string_switch_times = map(lambda x: str(x) + ' ', self._switch_times)
        return ' '.join(string_switch_times) + '\n'

    def __getitem__(self, item) -> int:
        return self._switch_times[item]

    def __len__(self) -> int:
        return len(self._switch_times)

    def __add__(self, other: int):
        self._switch_times.append(other)
