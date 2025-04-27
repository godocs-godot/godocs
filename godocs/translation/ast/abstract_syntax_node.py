
from abc import ABC, abstractmethod

class AbstractSyntaxNode(ABC):

  @abstractmethod
  def translate(self, translator) -> str:
    pass

