from abc import ABC, abstractmethod

from godocs.translation.ast.abstract_syntax_text_node import *
from godocs.translation.ast.abstract_syntax_tag_node import *

class SyntaxTranslator(ABC):

  @abstractmethod
  def translate_text(self, node: AbstractSyntaxTextNode) -> str:
    pass

  @abstractmethod
  def translate_tag(self, node: AbstractSyntaxTagNode) -> str:
    pass
