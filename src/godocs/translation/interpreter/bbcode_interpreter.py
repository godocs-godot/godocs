import re
from typing import TypedDict

from .interpreter import Interpreter
from godocs.translation import ast


class TagOptions(TypedDict):
    list: list[str]
    map: dict[str, str]


class BBCodeInterpreter(Interpreter):
    """
    `BBCodeInterpreter` is a specialized class that parses `BBCode`
    markup into an abstract syntax tree (AST) representation.

    Here's a list of tags this interpreter supports:
    - [b][/b] -> ``
    - [i][/i] -> ``
    - [u][/u] -> ``

    This interpreter supports a variety of `BBCode` tags,
    including formatting tags (e.g., [b], [i], [u]),
    reference tags (e.g., [class], [method]), and special tags
    (e.g., [br], [img], [url]).

    It converts recognized tags into corresponding AST nodes,
    handling both standalone and nested tags, and supports
    parsing of tag options and parameters.

    Methods:
      interpret(text: str) -> ast.TagNode:
        Parses the input BBCode text and returns the root AST node.
      parse_options(options: str) -> dict:
        Parses the options string from a BBCode tag and returns a dictionary with 'list' and 'map' keys for positional and key-value options.
      parse_reference_tag(el_match: re.Match[str]) -> ast.TagNode:
        Parses reference tags (e.g., [class], [method], [operator]) and returns the corresponding AST node.
      parse_tag(el_match: re.Match) -> ast.Node:
        Parses standalone tags (e.g., [br], [lb], [rb]) or delegates to parse_reference_tag for reference tags.
      parse_element(el_match: re.Match[str]) -> ast.Node:
        Parses a matched BBCode element, handling both standalone and paired tags, and returns the corresponding AST node.
      parse_text(text: str, root=ast.TagNode("root")) -> ast.TagNode:
        Recursively parses BBCode text, building and returning the AST rooted at the given node.
    Attributes:
      el_regex (str): Regular expression pattern used to match BBCode elements in the input text.
    """

    el_regex = r"\[(?P<name>\w+)(?P<options>[\S\s]*?)\](?:(?P<content>[\S\s]*?)\[(?P<closing>\/)\1\])?"

    def interpret(self, text: str) -> ast.TagNode:
        return self.parse_text(text)

    def parse_options(self, options: str) -> TagOptions:
        """
        Parses a string with the options of a `BBCode` tag and
        returns a `TagOptions` dictionary separating those options
        in a `"list"` and a `"map"`.

        Examples::

            parse_options("=https://github.com/nadjiel")
            # Would return:
            { 
                "list": [],
                "map": {
                    "": "=https://github.com/nadjiel"
                }
            }

            parse_options(" width=32 height=16")
            # Would return:
            { 
                "list": [],
                "map": {
                    "width": "32",
                    "height": "16"
                }
            }

            parse_options(" Color.operator *")
            # Would return:
            { 
                "list": [ "Color.operator", "*" ],
                "map": {}
            }
        """

        result: TagOptions = {
            "list": [],
            "map": {},
        }

        pairs = options.split(' ')

        for pair in pairs:
            if not pair:
                continue

            key_value = pair.split('=')
            key = key_value[0]

            if len(key_value) == 1:
                result["list"].append(key)
                continue

            value = key_value[1]

            result["map"][key] = value

        return result

    def parse_reference_tag(self, el_match: re.Match[str]) -> ast.TagNode:
        name = el_match.group("name")
        options = el_match.group("options")

        params = self.parse_options(options)

        result = ast.TagNode("tag")

        # Converts every possible reference to a "reference" Node.
        match name:
            case ("annotation"
                  | "constant"
                  | "enum"
                  | "member"
                  | "method"
                  | "constructor"
                  | "operator"
                  | "signal"
                  | "theme_item"):
                # Register data from references with format [<type> <name>].
                result.name = "reference"
                result.params = {
                    "type": name,
                    "name": params["list"][0],
                }

                # If the reference is an operator ([operator <name> <symbol>]),
                # also register its symbol.
                if name == "operator":
                    result.params["symbol"] = params["list"][1]

                return result
            case _: pass

        # If the reference is a [param <name>], converts to inline code.
        if name == "param":
            return ast.TagNode(
                "code", [ast.TextNode(params["list"][0])]
            )

        # If the reference is none of the above, assumes it is a Class reference.
        return ast.TagNode("reference", [], {
            "type": "class", "name": name
        })

    def parse_tag(self, el_match: re.Match[str]) -> ast.Node:
        """
        Parses a regex match of a text with a `BBCode`
        tag returning its equivalent in an AST `Node`.

        This method is only capable of parsing standalone tags,
        not full elements.

        With that said, the only such tags
        are the `[br]`, the `[lb]` and the `[rb]`.

        For full elements, see `parse_element`.
        """

        name = el_match.group("name")

        match name:
            # Returns a new line tag Node.
            case "br": return ast.TagNode("newline")
            # Returns a text Node with "[".
            case "lb": return ast.TextNode("[")
            # Returns a text Node with "]".
            case "rb": return ast.TextNode("]")
            case _: pass

        # If the tag isn't any of the above, it's assumed it is a reference tag,
        # (tags that point to a Class, a property etc).
        return self.parse_reference_tag(el_match)

    def parse_element(self, el_match: re.Match[str]) -> ast.Node:
        """
        Parses a regex match of a text with a `BBCode` element into
        an Abstract Syntax Tree `Node`.

        This method currently understands the following elements:
        - `[b][/b]`
        - `[i][/i]`
        - `[u][/u]`
        - `[s][/s]`
        - `[color][/color]`
        - `[font][/font]`
        - `[img][/img]`
        - `[url][/url]`
        - `[center][/center]`
        - `[kbd][/kbd]`
        - `[code][/code]`
        - `[codeblock][/codeblock]`

        Not counting these, this method also interprets the standalone tags
        supported by the `parse_tag` method.
        """

        # If the match doesn't have a closing tag, it is a standalone tag.
        if not el_match.group("closing"):
            return self.parse_tag(el_match)

        name = el_match.group("name")
        content = el_match.group("content")
        options = el_match.group("options")

        params = self.parse_options(options)

        element = ast.TagNode(name)

        match name:
            # Converts general markup to standard tag Nodes.
            # case 'p': element.name = "paragraph"
            case 'b': element.name = "bold"
            case 'i': element.name = "italic"
            case 'u': element.name = "underline"
            case 's': element.name = "strikethrough"
            case "color":
                element.name = "color"
                element.params["value"] = params["map"].get('', '')
            case "font":
                element.name = "font"
                element.params["url"] = params["map"].get('', '')
            case "img":
                element.name = "image"
                element.params["width"] = params["map"].get("width", '')
            case "url":
                element.name = "link"
                element.params["url"] = params["map"].get('', content)
            case "center":
                element.name = "alignment"
                element.params["x"] = "center"
            # For the below cases, don't parse the contents, as they aren't meant
            # to be parsed (they are either keyboard keys or code samples).
            case "kbd":
                element.name = "keyboard"
                element.children.append(ast.TextNode(content))
                return element
            case "code":
                element.name = "code"
                element.children.append(ast.TextNode(content))
                return element
            case "codeblock":
                element.name = "codeblock"
                element.params["language"] = params["map"].get("lang", '')
                element.children.append(ast.TextNode(content))
                return element
            case _: pass

        # If there is any content inside the element parsed, use parse_text to
        # parse it and append it to the element as root.
        # Since parse_text may use this own method, this can end up
        # being recursive.
        if content:
            element = self.parse_text(content, element)

        return element

    def parse_text(
        self,
        text: str,
        root: ast.TagNode | None = None,
    ) -> ast.TagNode:
        if root is None:
            root = ast.TagNode("root")

        text_start = 0
        text_end = len(text)

        # Searches all elements with the el_regex.
        el_matches = list(re.finditer(
            self.el_regex,
            text,
        ))

        # If no elements are found, the entire content is considered plain text.
        if not el_matches:
            root.children.append(ast.TextNode(text))
            return root

        prev_el_end = text_start

        # For each element found
        for i, el_match in enumerate(el_matches):
            el_start = el_match.start()
            el_end = el_match.end()

            # Parse the content prior to this element, if any.
            if el_start > prev_el_end:
                root.children.append(ast.TextNode(text[prev_el_end:el_start]))

            # Parse the element found, and, consequentially, its children.
            root.children.append(self.parse_element(el_match))

            # Parse the remaining contents, if any.
            if i == len(el_matches) - 1:
                if el_end < text_end:
                    root.children.append(ast.TextNode(text[el_end:]))

            prev_el_end = el_end

        return root
