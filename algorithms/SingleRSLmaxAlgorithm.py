import random
from typing import List

import numpy as np
from numpy import mean

from algorithms import Algorithm
from commons import RSTask, parse_to_task_value, SwitchTimes, parse_switch_times, parse_rs_task, timer


class SingleRSLmaxAlgorithm(Algorithm):
    time_factor = 1 / 4
    ready_factor = 0.1
    switch_factor = 40
    mean_switch_factor = 0.2
    deadline_factor = 0.8
    duration_factor = 1

    @classmethod
    def schedule_tasks(cls, file_name: str) -> List[int]:
        tasks = cls._open_task_file(file_name)
        for i in range(len(tasks)):
            tasks[i].set_index(i)
        algorithm = SingleRSLmaxAlgorithm()
        order = algorithm._run(tasks)
        max_delay = cls._validate(tasks, order)

        cls._save_to_output_file(file_name, max_delay, [order_item + 1 for order_item in order])
        print(f'Result score of {file_name}: \t {max_delay}')
        return order

    @timer
    def _run(self, tasks: List[RSTask]) -> List[int]:
        order = []
        sorted_tasks = sorted(tasks, key=lambda task: task.ready_time)
        additional_time = mean([task.duration_time for task in sorted_tasks]) * self.time_factor
        current_time = 0

        for i in range(len(sorted_tasks)):
            current_time = max(current_time, sorted_tasks[0].ready_time)

            possible_tasks: List[RSTask] = \
                [task for task in sorted_tasks if task.ready_time <= (current_time + additional_time)]
            if i == 0:
                selected_task = min(possible_tasks, key=lambda task:
                (self.deadline_factor * task.deadline_time)
                - (self.duration_factor * task.duration_time)
                + (self.ready_factor * max(0, (current_time - task.ready_time)))
                + (self.mean_switch_factor * task.switch_times.get_mean_time()))
            else:
                selected_task = min(possible_tasks, key=lambda task:
                (self.deadline_factor * task.deadline_time)
                - (self.duration_factor * task.duration_time)
                + (self.ready_factor * max(0, (current_time - task.ready_time)))
                + (self.switch_factor * tasks[order[-1]].switch_times[task.index])
                + (self.mean_switch_factor * task.switch_times.get_mean_time()))

            order.append(selected_task.index)
            sorted_tasks.remove(selected_task)
            if i > 1:
                current_time += tasks[order[-2]].switch_times[selected_task.index]
            current_time = max(selected_task.ready_time, current_time) + selected_task.duration_time
        return order

    @classmethod
    def generate(cls, file_prefix: str, instance_size: int):
        duration_times = parse_to_task_value(np.random.normal(30, 15, instance_size), 1)
        ready_times = parse_to_task_value(np.random.exponential(sum(duration_times) / 8, instance_size))
        deadline_times = ready_times + duration_times + parse_to_task_value(
            np.random.uniform(1, 3 * np.mean(duration_times), instance_size))
        tasks = [RSTask(int(ready_times[i]), int(duration_times[i]), int(deadline_times[i])) for i in
                 range(instance_size)]
        cls.generate_switch_times(tasks)
        cls._save_to_input_file(tasks, file_prefix, instance_size)

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
    def _save_to_input_file(cls, tasks: List[RSTask], file_prefix: str, instance_size: int):
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
        max_delay = cls._validate(tasks, results)
        print(f'Result score of {file_name}: \t {max_delay}')

    @classmethod
    def _validate(cls, tasks: List[RSTask], results: List[int]) -> int:
        current_moment = tasks[results[0]].ready_time + tasks[results[0]].duration_time
        max_delay = current_moment - tasks[results[0]].deadline_time
        for i in range(1, len(results)):
            current_moment += tasks[results[i - 1]].switch_times[results[i]]
            current_moment = max(current_moment, tasks[results[i]].ready_time)
            current_moment += tasks[results[i]].duration_time
            max_delay = max(max_delay, current_moment - tasks[results[i]].deadline_time)
        return max_delay
