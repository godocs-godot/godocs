from functools import reduce
from godocs.translation.translator import SyntaxTranslator as BaseTranslator
from godocs.translation import ast


class SyntaxTranslator(BaseTranslator):
    """
    This class is an example of how a custom translator can be implemented by
    extending the base :class:`~godocs.translation.translator.SyntaxTranslator`.

    By exposing a Python script exposing a class called `SyntaxTranslator`,
    one can pass its path to the `construct` command from the CLI via the
    `-t` or `--translator` option to use it as the translator
    when generating the documentation.
    """

    def translate_text(self, node: "ast.TextNode") -> str:
        return node.content

    def translate_tag(self, node: "ast.TagNode") -> str:
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
            case "italic": return f"_{content}_"
            case "paragraph": return content
            case "code": return f"`{content}`"
            case "codeblock": return self.make_codeblock(
                content,
                node.params.get("language", '')
            )
            case "link": return f"[{content}]({node.params.get("url", '')})"
            # make_code_member_ref(node.params.get("name", ''))
            case "reference": return node.params.get("name", '')
            case _: return ''

        return content

    @staticmethod
    def make_codeblock(content: str, language: str = '') -> str:
        header = "``` " + language
        footer = "```"

        return f"{header}\n{content}\n{footer}"
