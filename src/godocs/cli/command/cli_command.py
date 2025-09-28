from abc import ABC, abstractmethod
from typing import Any


class CLICommand(ABC):

    @abstractmethod
    def register(self, subparsers: Any):
        pass
