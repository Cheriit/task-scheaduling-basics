import random
from typing import List

import numpy as np

from algorithms import Algorithm
from commons import RSTask, parse_to_task_value, SwitchTimes, parse_switch_times, parse_rs_task


class SingleRSLmaxAlgorithm(Algorithm):

    @classmethod
    def generate(cls, file_prefix: str, instance_size: int):
        ready_times = parse_to_task_value(np.random.exponential(instance_size / 2, instance_size))
        duration_times = parse_to_task_value(np.random.normal(10, 4, instance_size), 1)
        deadline_times = ready_times + duration_times + parse_to_task_value(np.random.uniform(1, 20))
        tasks = [RSTask(ready_times[i], duration_times[i], deadline_times[i]) for i in range(instance_size)]
        cls.generate_switch_times(tasks)
        cls._save_to_file(tasks, file_prefix, instance_size)

    @classmethod
    def generate_switch_times(cls, tasks):
        for i in range(len(tasks)):
            switch_times = []
            for j in range(len(tasks)):
                if i == j:
                    switch_times.append(0)
                else:
                    switch_times.append(random.randint(0, min(tasks[i].duration_time, tasks[j].duration_time)))
            tasks[i].switch_times = SwitchTimes(switch_times)

    @classmethod
    def _save_to_file(cls, tasks: List[RSTask], file_prefix: str, instance_size: int):
        file = open(f'in/{file_prefix}_{instance_size}.txt', 'w')
        file.write(f'{instance_size}\n')
        for task in tasks:
            file.write(str(task))
        for task in tasks:
            file.write(str(task.switch_times))

    @classmethod
    def _open_task_file(cls, file_name: str) -> List[RSTask]:
        file = open(f'in/{file_name}')
        size = int(file.readline())
        tasks = []
        for i in range(size):
            tasks.append(parse_rs_task(file.readline()))
        for task in tasks:
            task.switch_times = parse_switch_times(file.readline())
        return tasks

    @classmethod
    def validate(cls, file_name: str):
        tasks = cls._open_task_file(file_name)
        results = SingleRSLmaxAlgorithm.open_result_file(file_name)
        if len(tasks) != len(results):
            raise ValueError('Lack of coherency between input and result file')
        current_moment = tasks[results[0]].ready_time + tasks[results[0]].duration_time
        max_delay = current_moment - tasks[results[0]].deadline_time
        for i in range(1, len(results)):
            current_moment += tasks[results[i-1]].switch_times[results[i]]
            current_moment = max(current_moment, tasks[results[i]].ready_time)
            current_moment += tasks[results[i]].duration_time
            max_delay = max(max_delay, current_moment - tasks[results[i]].deadline_time)
        print(f'Result score of {file_name}: \t {max_delay}')
