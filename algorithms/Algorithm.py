from abc import ABC, abstractmethod
from typing import List

from commons import Task


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
    def _save_to_input_file(cls, tasks: List[Task], file_prefix: str, instance_size: int):
        pass

    @classmethod
    @abstractmethod
    def _open_task_file(cls, file_name: str) -> List[Task]:
        pass

    @classmethod
    @abstractmethod
    def open_result_file(cls, file_name: str) -> List[int]:
        pass

    @classmethod
    @abstractmethod
    def generate_mock_result_file(cls, file_name):
        pass

    @classmethod
    @abstractmethod
    def _save_to_output_file(cls, file_name: str, value: int, tasks: List[int]):
        pass

    @abstractmethod
    def schedule_tasks(self, file_name: str) -> List[int]:
        pass
