import re

from .syntax_interpreter import SyntaxInterpreter
from godocs.translation.ast import (
  AbstractSyntaxNode,
  AbstractSyntaxTagNode,
  AbstractSyntaxTextNode,
)

class BBCodeSyntaxInterpreter(SyntaxInterpreter):

  el_regex = r"\[(?P<name>\w+)(?P<options>[\S\s]*?)\](?:(?P<content>[\S\s]*?)\[(?P<closing>\/)\1\])?"

  def interpret(self, text: str) -> AbstractSyntaxTagNode:
    return self.parse_text(text)

  def parse_options(self, options: str) -> dict:
    result = {
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

  def parse_reference_tag(self, el_match: re.Match[str]) -> AbstractSyntaxTagNode:
    name = el_match.group("name")
    options = el_match.group("options")

    params = self.parse_options(options)

    result = AbstractSyntaxTagNode("tag")

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

    # If the reference is a [param <name>], converts to inline code.
    if name == "param":
      return AbstractSyntaxTagNode(
        "code", [ AbstractSyntaxTextNode(params["list"][0]) ]
      )
    
    # If the reference is none of the above, assumes it is a Class reference.
    return AbstractSyntaxTagNode("reference", [], {
      "type": "class", "name": name
    })

  def parse_tag(self, el_match: re.Match) -> AbstractSyntaxNode:
    name = el_match.group("name")

    match name:
   		# Returns a new line tag Node.
      case "br": return AbstractSyntaxTagNode("newline")
   		# Returns a text Node with "[".
      case "lb": return AbstractSyntaxTextNode("[")
   		# Returns a text Node with "]".
      case "rb": return AbstractSyntaxTextNode("]")
    
    # If the tag isn't any of the above, it's assumed it is a reference tag,
    # (tags that point to a Class, a property etc).
    return self.parse_reference_tag(el_match)

  def parse_element(self, el_match: re.Match[str]) -> AbstractSyntaxNode:
    # If the match doesn't have a closing tag, it is a standalone tag.
    if not el_match.group("closing"):
      return self.parse_tag(el_match)
      
    name = el_match.group("name")
    content = el_match.group("content")
    options = el_match.group("options")

    params = self.parse_options(options)

    element = AbstractSyntaxTagNode(name)

    match name:
      # Converts general markup to standard tag Nodes.
      case 'p': element.name = "paragraph"
      case 'b': element.name = "bold"
      case 'i': element.name = "italics"
      case 's': element.name = "strikethrough"
      case 'u': element.name = "underline"
      case "center":
        element.name = "alignment"
        element.params["orientation"] = "horizontal"
        element.params["direction"] = "center"
      case "color":
        element.name = "color"
        element.params["value"] = params["map"].get('', '')
      case "font":
        element.name = "font"
        element.params["path"] = params["map"].get('', '')
      case "img":
        element.name = "image"
        element.params["width"] = params["map"].get("width", '')
      case "url":
        element.name = "link"
        element.params["url"] = params["map"].get('', content)
      # For the below cases, don't parse the contents, as they aren't meant
      # to be parsed (they are either keyboard keys or code samples).
      case "kbd":
        element.name = "keyboard"
        element.children.append(AbstractSyntaxTextNode(content))
        return element
      case "code":
        element.name = "code"
        element.children.append(AbstractSyntaxTextNode(content))
        return element
      case "codeblock":
        element.name = "codeblock"
        element.params["language"] = params["map"].get("lang", '')
        element.children.append(AbstractSyntaxTextNode(content))
        return element

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
      root = AbstractSyntaxTagNode("root"),
  ) -> AbstractSyntaxTagNode:
    text_start = 0
    text_end = len(text)

    # Searches all elements with the el_regex.
    el_matches = list(re.finditer(
      self.el_regex,
      text,
    ))

    # If no elements are found, the entire content is considered plain text.
    if not el_matches:
      root.children.append(AbstractSyntaxTextNode(text))
      return root

    prev_el_end = text_start

    # For each element found
    for i, el_match in enumerate(el_matches):
      el_start = el_match.start()
      el_end = el_match.end()

      # Parse the content prior to this element, if any.
      if el_start > prev_el_end:
        root.children.append(AbstractSyntaxTextNode(text[prev_el_end:el_start]))
      
      # Parse the element found, and, consequentially, its children.
      root.children.append(self.parse_element(el_match))

      # Parse the remaining contents, if any.
      if i == len(el_matches) - 1:
        if el_end < text_end:
          root.children.append(AbstractSyntaxTextNode(text[el_end:]))
      
      prev_el_end = el_end

    return root
