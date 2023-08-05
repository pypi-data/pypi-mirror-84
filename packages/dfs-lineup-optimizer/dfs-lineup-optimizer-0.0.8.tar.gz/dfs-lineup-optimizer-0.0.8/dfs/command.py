from abc import ABC, abstractmethod
from argparse import Namespace


class Command(ABC):
    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def add_parser(self, subparsers):
        pass

    @abstractmethod
    def execute(self, args=Namespace):
        pass

    @property
    def name(self) -> str:
        return self._name