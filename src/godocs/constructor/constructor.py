from abc import ABC, abstractmethod
from os import PathLike
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from godocs.parser.context_creator import DocContext, Class


class ConstructorContext(DocContext):
    current_class: Class


class Constructor(ABC):

    @abstractmethod
    def construct(self, context: ConstructorContext, path: str | PathLike[str]):
        pass
