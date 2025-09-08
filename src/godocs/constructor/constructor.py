from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from godocs.parser.context_creator import DocContext


class TemplateMap(TypedDict):
    class_reference: str
    index: str
    others: str


class Constructor(ABC):

    @abstractmethod
    def construct(self, context: "DocContext", templates: TemplateMap, path: str):
        pass
