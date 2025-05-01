from .abstract_syntax_node import AbstractSyntaxNode

class AbstractSyntaxTextNode(AbstractSyntaxNode):

  def __init__(self, content: str):
    self.content = content

  def translate(self, translator) -> str:
    return translator.translate_text(self)

  def __str__(self) -> str:
    return f'"{self.content}"'
