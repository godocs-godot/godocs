
from abc import ABC, abstractmethod

from godocs.translation.ast.abstract_syntax_tag_node import *

class SyntaxInterpreter(ABC):

  @abstractmethod
  def interpret(self, text: str) -> AbstractSyntaxTagNode:
    pass

