import random
from math import floor
from typing import List, Tuple

import numpy as np
from numpy import mean

from algorithms import Algorithm
from commons import RWTask, parse_to_task_value, parse_rw_task, parse_input_string, Machine


class Q4RSumWUAlgorithm(Algorithm):
    time_factor = 0
    ready_factor = 0.25
    ready_time_factor = 0
    deadline_factor = 3
    duration_factor = 1
    priority_factor = 3
    ratio_factor = 0

    @classmethod
    def schedule_tasks(cls, file_name: str):
        machines, tasks = cls._open_task_file(file_name)
        for i in range(len(tasks)):
            tasks[i].set_index(i)
        algorithm = Q4RSumWUAlgorithm()
        score = algorithm._run(machines, tasks)
        cls._save_to_output_file(file_name, score, machines)
        print(f'Result score of {file_name}: \t {score}')

    @classmethod
    def _save_to_output_file(cls, file_name: str, value: float, machines: List[Machine]):
        file = open(f'out/{file_name}', 'w')
        file.write(f'{value}\n')
        for i in range(len(machines)):
            file.write(f'{machines[i]}\n')

    def _run(self, machines: List[Machine], tasks: List[RWTask]) -> float:
        delayed_tasks = []
        sorted_tasks = sorted(tasks, key=lambda task: task.ready_time)
        additional_time = mean([task.duration_time for task in sorted_tasks]) * self.time_factor

        for task in sorted_tasks:
            task.score = (self.deadline_factor * task.deadline_time)\
                         - (self.duration_factor * task.duration_time)\
                         - (self.priority_factor * task.priority)

        max_speedup = max(machines, key=lambda machine: machine.current_time).speedup
        fastest_freed_machine = min(machines, key=lambda machine: machine.current_time)
        while len(sorted_tasks) > 0:
            current_time = max(fastest_freed_machine.current_time, sorted_tasks[0].ready_time)
            possible_tasks = [task for task in sorted_tasks if task.ready_time <= current_time + additional_time]

            select_task = min(possible_tasks, key=lambda task: task.score
                + self.ready_time_factor * (task.deadline_time - max(current_time, task.ready_time))
                + self.ready_factor * max(0, (current_time - task.ready_time)))

            fastest_freed_machine.add_task(select_task)
            fastest_freed_machine = min(machines, key=lambda machine: machine.current_time)
            sorted_tasks.remove(select_task)

            delayed_tasks += [task for task in sorted_tasks
                              if task.deadline_time < fastest_freed_machine.current_time + (task.duration_time / max_speedup)]
            sorted_tasks = [task for task in sorted_tasks
                            if task.deadline_time >= fastest_freed_machine.current_time + (task.duration_time / max_speedup)]

        score = 0
        for task in delayed_tasks:
            machines[0].add_task(task)
            score += task.priority
        return score

    @classmethod
    def generate(cls, file_prefix: str, instance_size: int):
        mean_time = 40

        duration_times = parse_to_task_value(np.random.normal(mean_time, 15, instance_size), 1)
        ready_times = parse_to_task_value(np.random.uniform(0, sum(duration_times) * 1 / 6, instance_size))
        for i in range(floor(mean_time * 0.1)):
            ready_times[random.randint(0, instance_size - 1)] = 0
        priorities = []
        for duration in duration_times:
            if duration > mean_time:
                priorities.append(np.random.uniform(40, 80))
            else:
                priorities.append(np.random.uniform(1, 60))
        deadline_times = ready_times + duration_times + parse_to_task_value(
            np.random.exponential(np.mean(duration_times) / 4, instance_size))
        tasks = [RWTask(int(ready_times[i]), int(duration_times[i]), int(deadline_times[i]), int(priorities[i])) for i
                 in
                 range(instance_size)]
        cls._save_to_input_file(tasks, file_prefix, instance_size)

    @classmethod
    def _save_to_input_file(cls, tasks: List[RWTask], file_prefix: str, instance_size: int):
        file = open(f'in/{file_prefix}_{instance_size}.txt', 'w')
        file.write(f'{instance_size}\n')
        speedups = [random.randint(1, 10), random.randint(1, 10), 1, random.randint(1, 10)]
        random.shuffle(speedups)
        file.write(f'{speedups[0]} {speedups[1]} {speedups[2]} {speedups[3]}\n')
        for task in tasks:
            file.write(str(task))

    @classmethod
    def _open_task_file(cls, file_name: str) -> Tuple[List[Machine], List[RWTask]]:
        file = open(f'in/{file_name}')
        size = int(file.readline())
        tasks = []
        machines = []
        speedups = file.readline().replace('\n', '').strip().split(' ')
        for speedup in speedups:
            machines.append(Machine(float(speedup)))
        for i in range(size):
            tasks.append(parse_rw_task(file.readline()))
        return machines, tasks

    @classmethod
    def validate(cls, file_name: str):
        machines, tasks = cls._open_task_file(file_name)
        results = cls.open_result_file(file_name)
        max_delay = cls._validate(machines, tasks, results)
        print(f'Result score of {file_name}: \t {max_delay}')

    @classmethod
    def _validate(cls, machines: List[Machine], tasks: List[RWTask], results: List[List[int]]) -> int:
        score = 0
        for i in range(len(results)):
            machine = machines[i]
            for j in results[i]:
                task = tasks[j]
                machine.add_task(task)
                if machine.current_time > task.deadline_time:
                    score += task.priority
        return score

    @classmethod
    def open_result_file(cls, file_name: str) -> List[List[int]]:
        file = open(f'out/{file_name}', 'r')
        file.readline()
        tasks = []
        for i in range(4):
            tasks.append(list(map(lambda x: int(x) - 1, parse_input_string(file.readline()))))
        return tasks

    @classmethod
    def generate_mock_result_file(cls, file_name):
        input_file = open(f'in/{file_name}', 'r')
        file = open(f'out/{file_name}', 'w')
        instance_size = floor(float(input_file.readline()))
        processes_per_machine = floor(instance_size / 4)
        process_counter = 1
        file.write(f'{instance_size}\n')
        for i in range(3):
            for j in range(processes_per_machine):
                file.write(f'{process_counter} ')
                process_counter += 1
            file.write('\n')
        while process_counter <= instance_size:
            file.write(f'{process_counter} ')
            process_counter += 1
