from abc import ABC, abstractmethod


class Algorithm(ABC):

    @abstractmethod
    def generate(self, file_prefix: str, instance_size: int):
        pass

    @abstractmethod
    def validate(self):
        pass
