from abc import ABC, abstractmethod

class Constructor(ABC):

  @abstractmethod
  def construct(self, context: dict, build_path: str):
    pass
