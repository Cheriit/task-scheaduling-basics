from abc import ABC, abstractmethod
from math import floor
from typing import List

from commons import parse_input_string, Task


class Algorithm(ABC):

    @classmethod
    @abstractmethod
    def generate(cls, file_prefix: str, instance_size: int):
        pass

    @classmethod
    @abstractmethod
    def validate(cls, file_name: str):
        pass

    @classmethod
    @abstractmethod
    def _save_to_file(cls, tasks: List[Task], file_prefix: str, instance_size: int):
        pass

    @classmethod
    @abstractmethod
    def _open_task_file(cls, file_name: str) -> List[Task]:
        pass

    @staticmethod
    def open_result_file(file_name: str) -> List[int]:
        file = open(f'out/{file_name}', 'r')
        file.readline()
        return list(map(lambda x: int(x), parse_input_string(file.readline())))

    @staticmethod
    def generate_mock_result_file(file_name):
        input_file = open(f'in/{file_name}', 'r')
        file = open(f'out/{file_name}', 'w')
        instance_size = floor(float(input_file.readline()))
        file.write(f'{instance_size}\n')
        for i in range(instance_size):
            file.write(f'{i} ')
