from abc import ABC, abstractmethod

from godocs.translation.ast import (
    TextNode,
    TagNode,
)


class SyntaxTranslator(ABC):

    @abstractmethod
    def translate_text(self, node: TextNode) -> str:
        pass

    @abstractmethod
    def translate_tag(self, node: TagNode) -> str:
        pass
