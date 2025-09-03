from abc import ABC, abstractmethod
from godocs.translation.translator import SyntaxTranslator


class Node(ABC):
    """
    Abstract base class representing a node in an abstract syntax tree used
    for syntax translation (AST).

    Subclasses must implement the `translate` method, which defines how the node should be
    translated using a provided `SyntaxTranslator`.
    """

    @abstractmethod
    def translate(self, translator: SyntaxTranslator) -> str:
        """
        Abstract method to translate this `Node` using a given `translator`.
        """
        pass
