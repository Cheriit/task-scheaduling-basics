import numpy as np


def parse_to_task_value(array: np.array, min_value: int = 0) -> np.array:
    return np.clip(np.floor(array), min_value, None)
