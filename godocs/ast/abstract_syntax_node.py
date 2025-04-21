
class AbstractSyntaxNode:

  def translate(self, translator) -> str:
    return ""

  def __str__(self) -> str:
    return "<>"
