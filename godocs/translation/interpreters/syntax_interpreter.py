from abc import ABC, abstractmethod

from ..ast import AbstractSyntaxTagNode

class SyntaxInterpreter(ABC):

  @abstractmethod
  def interpret(self, text: str) -> AbstractSyntaxTagNode:
    pass
