
from textwrap import indent

from godocs.translation.ast.abstract_syntax_node import *

class AbstractSyntaxTagNode(AbstractSyntaxNode):

  def __init__(
      self,
      name: str,
      children: list[AbstractSyntaxNode] = None,
      params: dict[str, str] = None,
  ):
    if children is None:
      children = []
    if params is None:
      params = {}
    
    self.name = name
    self.children = children
    self.params = params

  def translate(self, translator) -> str:
    return translator.translate_tag(self)

  def stringify_params(self) -> str:
    result = ""

    for i, key in enumerate(self.params):
      value = self.params[key]

      result += f"{key}={value}"
		
      if i < len(self.params) - 1:
        result += ", "
    
    return result

  def stringify_children(self) -> str:
    result = ""

    for i, child in enumerate(self.children):
      result += str(child)
		
      if i < len(self.children) - 1:
        result += ",\n"
    
    return result

  def __str__(self) -> str:
    result = f"<{self.name}"

    if not len(self.params) == 0:
      result += f" {self.stringify_params()}"
    
    if not len(self.children) == 0:
      result += indent(f"\n{self.stringify_children()}\n", "\t")

    result += '>'

    return result
