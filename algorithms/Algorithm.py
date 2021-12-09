from abc import ABC, abstractmethod


class Algorithm(ABC):

    @classmethod
    @abstractmethod
    def generate(cls, file_prefix: str, instance_size: int):
        pass

    @abstractmethod
    def schedule_tasks(self, file_name: str):
        pass

    @classmethod
    @abstractmethod
    def validate(cls, file_name: str):
        pass

    @classmethod
    @abstractmethod
    def create_input_file(cls, tasks, file_prefix: str, instance_size: int):
        pass

    @classmethod
    @abstractmethod
    def open_input_file(cls, file_name: str):
        pass

    @classmethod
    @abstractmethod
    def open_result_file(cls, file_name: str):
        pass

    @classmethod
    @abstractmethod
    def create_output_file(cls, file_name: str, value: int, tasks):
        pass

    @classmethod
    @abstractmethod
    def create_mock_result_file(cls, file_name):
        pass
