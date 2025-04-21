
from godocs.ast.abstract_syntax_node import *

class AbstractSyntaxTextNode(AbstractSyntaxNode):

  content: str

  def __init__(self, content):
    self.content = content

  def translate(self, translator) -> str:
    return translator.translate_text(self)

  def __str__(self) -> str:
    return f'"{self.content}"'
