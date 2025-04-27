from functools import reduce

from godocs.translation.translators.syntax_translator import *
from godocs.filters import make_code_member_ref

class RSTSyntaxTranslator(SyntaxTranslator):

  def make_directive(
      self,
      name: str,
      args: list[str] = None,
      options: dict[str, str] = None,
      content: str = '',
  ) -> str:
    if args is None:
      args = []
    if options is None:
      options = {}
    
    name_output = name

    args_output = reduce(
      lambda prev, next: prev + next + ' ',
      args,
      '',
    )

    options_output = ''

    for i, option in enumerate(options):
      value = options[option]

      options_output += f":{option}: {value}"

      if i < len(options) - 1:
        options_output += "\n"
    
    if options_output:
      options_output = indent(options_output, "   ")

    content_output = indent(content, "   ")

    result = f".. {name_output}::"

    if args_output:
      result += f" {args_output}"
    if options_output:
      result += f"\n{options_output}"
    if content_output:
      result += f"\n\n{content_output}"

    return result

  def make_codeblock(self, content: str, language: str = '') -> str:
    return self.make_directive("codeblock", [ language ], {}, content)

  def translate_text(self, node: AbstractSyntaxTextNode) -> str:
    return node.content

  def translate_tag(self, node: AbstractSyntaxTagNode) -> str:
    # First of all, translates the children of the node received.
    content = reduce(
      lambda prev, next: prev + next.translate(self),
      node.children,
      '',
    )

    # Depending on the node name, the resultant syntax will change.
    match node.name:
      case "root": return content
      case "bold": return f"**{content}**"
      case "newline": return f"\n"
      case "italics": return f"*{content}*"
      case "paragraph": return content
      case "code": return f"``{content}``"
      case "codeblock": return self.make_codeblock(
        content,
        node.params.get("language", '')
      )
      case "link": return f"{content} <{node.params.get("url", '')}>_"
      case "reference": return make_code_member_ref(node.params.get("name", ''))

    return content
