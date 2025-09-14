from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from godocs.parser.context_creator import DocContext


class Constructor(ABC):

    @abstractmethod
    def construct(self, context: "DocContext", path: str):
        pass
