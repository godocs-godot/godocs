from abc import ABC, abstractmethod

from ..ast import (
  AbstractSyntaxTextNode,
  AbstractSyntaxTagNode,
)

class SyntaxTranslator(ABC):

  @abstractmethod
  def translate_text(self, node: AbstractSyntaxTextNode) -> str:
    pass

  @abstractmethod
  def translate_tag(self, node: AbstractSyntaxTagNode) -> str:
    pass
