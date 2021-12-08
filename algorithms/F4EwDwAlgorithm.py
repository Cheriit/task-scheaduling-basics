from math import floor, ceil
from typing import List, Tuple

import numpy as np

from algorithms import Algorithm
from commons import parse_to_task_value, parse_input_string, FlowTask, parse_flow_task


def perform_task(machines: List[int], task: FlowTask) -> int:
    machines[0] += task.times[0]
    for i in range(1, len(task.times)):
        machines[i] = max(machines[i - 1], machines[i]) + task.times[i]
    return machines[-1]


def calculate_end_time(machines: List[int], task: FlowTask) -> int:
    current_time = machines[0] + task.times[0]
    for i in range(1, len(task.times)):
        current_time = max(current_time, machines[i]) + task.times[i]
    return current_time


class F4EwDwAlgorithm(Algorithm):

    @classmethod
    def schedule_tasks(cls, file_name: str) -> float:
        tasks = cls.open_input_file(file_name)
        for i in range(len(tasks)):
            tasks[i].set_index(i)
        algorithm = F4EwDwAlgorithm()
        task_order, score = algorithm._run(tasks)
        cls.create_output_file(file_name, score, task_order)
        print(f'Result score of {file_name}: \t {score}')
        return score

    @classmethod
    def create_output_file(cls, file_name: str, score: float, task_order: List[FlowTask]):
        file = open(f'out/{file_name}', 'w')
        file.write(f'{score}\n')
        file.write(" ".join([str(x) for x in task_order]))

    def _run(self, tasks: List[FlowTask]) -> Tuple[List[int], float]:
        sorted_tasks = sorted(tasks, key=lambda task: task.ready_time)
        score = 0
        task_order = []
        for task in sorted_tasks:
            task.score = 0

        while len(sorted_tasks) > 0:
            # Priority - delayed tasks -> They will grow! Split to 2 arrays - better delay and better early ?
            pass

        return task_order, score

    @classmethod
    def generate(cls, file_prefix: str, instance_size: int):
        weight_divider = 3 / 4

        mean_time_unit = 10
        scale_time_unit = 5

        high_weight_range = 40
        low_weight_range = 20

        duration_times = np.array((
            parse_to_task_value(np.random.normal(mean_time_unit * 3, scale_time_unit * 2, instance_size), 1),
            parse_to_task_value(np.random.normal(mean_time_unit * 1, scale_time_unit * 1, instance_size), 1),
            parse_to_task_value(np.random.normal(mean_time_unit * 2, scale_time_unit * 3, instance_size), 1),
            parse_to_task_value(np.random.normal(mean_time_unit * 3, scale_time_unit * 5, instance_size), 1)
        ))

        earliness_weights = np.concatenate((
            parse_to_task_value(np.random.normal(high_weight_range, 15, int(floor(instance_size * weight_divider))), 1),
            parse_to_task_value(np.random.normal(low_weight_range, 5, int(ceil(instance_size * (1 - weight_divider)))), 1)
        ))

        delay_weights = np.concatenate((
            parse_to_task_value(np.random.normal(high_weight_range, 15, int(floor(instance_size * weight_divider))), 1),
            parse_to_task_value(np.random.normal(low_weight_range, 5, int(ceil(instance_size * (1 - weight_divider)))), 1)
        ))

        max_sum = max([
            sum(duration_times[0]),
            sum(duration_times[1]),
            sum(duration_times[2]),
            sum(duration_times[3])
        ])

        deadline_times = [
            sum(duration_times[:, i]) + parse_to_task_value(np.random.uniform(0, max_sum))
            for i in range(instance_size)
        ]

        tasks = [
            FlowTask(duration_times[:, i], int(deadline_times[i]), int(earliness_weights[i]), int(delay_weights[i])) for
            i in range(instance_size)]
        cls.create_input_file(tasks, file_prefix, instance_size)

    @classmethod
    def create_input_file(cls, tasks: List[FlowTask], file_prefix: str, instance_size: int):
        file = open(f'in/{file_prefix}_{instance_size}.txt', 'w')
        file.write(f'{instance_size}\n')
        for task in tasks:
            file.write(str(task))

    @classmethod
    def open_input_file(cls, file_name: str) -> List[FlowTask]:
        file = open(f'in/{file_name}')
        size = int(file.readline())
        tasks = []
        for i in range(size):
            tasks.append(parse_flow_task(file.readline()))
        return tasks

    @classmethod
    def validate(cls, file_name: str):
        tasks = cls.open_input_file(file_name)
        score, task_order = cls.open_result_file(file_name)
        calculated_score = cls._validate(tasks, task_order)
        if calculated_score != score:
            print(f'ERROR - inconsistent score')
        print(f'Result score of {file_name}: \t {calculated_score}')

    @classmethod
    def _validate(cls, tasks: List[FlowTask], results: List[int]) -> int:
        score = 0
        machine_times = [0, 0, 0, 0]
        for i in range(len(results)):
            task = tasks[i]
            end_time = perform_task(machine_times, task)
            time_diff = task.deadline_time - end_time
            if time_diff > 0:
                score += time_diff * task.delay_weight
            elif time_diff < 0:
                score -= time_diff * task.earliness_weight
        return score

    @classmethod
    def open_result_file(cls, file_name: str) -> Tuple[float, list[int]]:
        file = open(f'out/{file_name}', 'r')
        score = float(file.readline().strip())
        return score, list(map(lambda x: int(x) - 1, parse_input_string(file.readline())))

    @classmethod
    def create_mock_result_file(cls, file_name):
        input_file = open(f'in/{file_name}', 'r')
        file = open(f'out/{file_name}', 'w')
        instance_size = floor(float(input_file.readline()))
        file.write('0\n')
        file.write(" ".join([str(x + 1) for x in range(instance_size)]))
