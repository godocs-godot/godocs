from xml.etree.ElementTree import ElementTree, Element
import xml.etree.ElementTree as ET

from .types import XMLNode, XMLDoc, Property, Method


def get_class_node(class_name: str, docs: list[XMLDoc]) -> XMLNode | None:
    for doc in docs:
        root = doc.getroot()

        if root.attrib.get("name") == class_name:
            return root

    return None


def parse_inheritage(root: XMLNode, docs: list[XMLDoc]) -> list[str]:
    result: list[str] = []

    parent_name = root.attrib.get("inherits", '')

    while parent_name != '':
        result.append(parent_name)

        parent = get_class_node(parent_name, docs)

        if parent is None:
            break

        parent_name = parent.attrib.get("inherits", '')

    return result


def parse_property(node: XMLNode) -> Property:
    """
    Parses a member node into a dict.

    Member node structure::

        <member name="color" type="Color" setter="set_color" getter="get_color" default="null">
          Description
        </member>

    Return structure::

        result = {
            "name": "color",
            "type": "Color",
            "default": "null",
            "description": "Description",
        }
    """

    result: Property = {
        "name": '',
        "type": '',
        "default": '',
        "description": '',
    }

    result["name"] = node.attrib.get("name", '')
    result["type"] = node.attrib.get("type", '')
    result["default"] = node.attrib.get("default", '')
    result["description"] = node.text.strip() if node.text is not None else ''

    return result


def parse_method(node: XMLNode) -> Method:
    """
    Parses a method node into a dict.

    Method node structure::

        <method name="add">
          <return type="int" />
          <param index="0" name="num1" type="int" />
          <param index="1" name="num2" type="int" />
          <description>
            Description
          </description>
        </method>

    Return structure::

        result = {
          "name": "add",
          "type": "int",
          "args": [
            {
              "name": "num1",
              "type": "int",
              "default": "",
              "description": "",
            },
            {
              "name": "num2",
              "type": "int",
              "default": "",
              "description": "",
            },
          ],
          "description": "Description",
        }
    """

    result: Method = {
        "name": '',
        "type": '',
        "args": [],
        "description": '',
    }

    result["name"] = node.attrib.get("name", '')
    result["type"] = node.find("return").attrib.get("type", '')  # type: ignore
    result["description"] = node \
        .find("description") \
        .text.strip() if node.text is not None else ''  # type: ignore

    for arg in node.findall("param"):
        result["args"].append(parse_property(arg))

    return result


# def parse_signal(node: Element) -> dict[str]:
#     result = {
#         "name": '',
#         "args": [],
#         "description": '',
#     }

#     result["name"] = node.attrib.get("name", '')
#     result["description"] = node.find(
#         "description").text.strip() if node.text is not None else ''

#     for arg in node.findall("param"):
#         result["args"].append(parse_property(arg))

#     return result


# def parse_constant(node: Element) -> dict[str, str]:
#     result = {
#         "name": '',
#         "value": '',
#         "description": '',
#     }

#     result["name"] = node.attrib.get("name", '')
#     result["value"] = node.attrib.get("value", '')
#     result["description"] = node.text.strip() if node.text is not None else ''

#     return result


# def parse_enum(name, values: list) -> dict[str, str]:
#     result = {
#         "name": '',
#         "values": [],
#         "description": '',
#     }

#     result["name"] = name

#     for value in values:
#         result["values"].append(parse_constant(value))

#     # result["description"] =  There's no way to get enum descriptions with doctool

#     return result


# def parse_theme_item(node: Element) -> dict[str, str]:
#     result = {
#         "name": '',
#         "data_type": '',
#         "type": '',
#         "default": '',
#         "description": '',
#     }

#     result["name"] = node.attrib.get("name", '')
#     result["data_type"] = node.attrib.get("data_type", '')
#     result["type"] = node.attrib.get("type", '')
#     result["default"] = node.attrib.get("default", '')
#     result["description"] = node.text.strip() if node.text is not None else ''

#     return result


# def parse_properties(node: Element) -> list[dict[str, str]]:
#     result = []

#     for property in node:
#         if property.text is None or property.text.strip() == '':
#             continue

#         result.append(parse_property(property))

#     return result


# def parse_methods(node: Element) -> list[dict[str, str]]:
#     result = []

#     for method in node.findall("method"):
#         description = method.find("description").text

#         if description is None or description.strip() == '':
#             continue

#         result.append(parse_method(method))

#     return result


# def parse_signals(node: Element) -> list[dict[str, str]]:
#     result = []

#     for signal in node.findall("signal"):
#         description = signal.find("description").text

#         if description is None or description.strip() == '':
#             continue

#         result.append(parse_signal(signal))

#     return result


# def parse_constants(node: Element) -> list[dict[str, str]]:
#     result = []

#     for constant in node.findall("constant"):
#         if constant.text is None or constant.text.strip() == '':
#             continue
#         if constant.attrib.get("enum", '') != '':
#             continue

#         result.append(parse_constant(constant))

#     return result


# def parse_enums(node: Element) -> list[dict[str, str]]:
#     result = []

#     enums = {}

#     for constant in node.findall("constant"):
#         enum_name = constant.attrib.get("enum", '')

#         if constant.text is None or constant.text.strip() == '':
#             continue
#         if enum_name == '':
#             continue

#         if enums.get(enum_name) is None:
#             enums[enum_name] = []

#         enums[enum_name].append(constant)

#     for enum in enums:
#         values = enums[enum]

#         result.append(parse_enum(enum, values))

#     return result


# def parse_theme_items(node: Element) -> list[dict[str, str]]:
#     result = []

#     for theme_item in node:
#         if theme_item.text is None or theme_item.text.strip() == '':
#             continue

#         result.append(parse_theme_item(theme_item))

#     return result


# def parse_class(root: Element, docs: list[ElementTree]) -> dict[str]:
#     result = {
#         "name": '',
#         "inheritage": [],
#         "brief_description": '',
#         "description": '',
#         "properties": [],
#         "methods": [],
#         "signals": [],
#         "constants": [],
#         "enums": [],
#         "theme_items": [],
#     }

#     result["name"] = root.attrib.get("name", '')
#     result["inheritage"] = parse_inheritage(root, docs)

#     for node in root:
#         match node.tag:
#             case "members": result["properties"] = parse_properties(node)
#             continue
#             case "methods": result["methods"] = parse_methods(node)
#             continue
#             case "signals": result["signals"] = parse_signals(node)
#             continue
#             case "constants":
#                 result["constants"] = parse_constants(node)
#                 result["enums"] = parse_enums(node)
#                 continue
#             case "theme_items": result["theme_items"] = parse_theme_items(node)

#     return result


# def create(
#         docs: list[ElementTree[Element[str]]],
#         options: dict[str, str] | None = None
# ) -> dict[str, str]:
#     if options is None:
#         options = {}

#     result = {
#         "options": options,
#         "classes": [],
#     }

#     for doc in docs:
#         root = doc.getroot()

#         result["classes"].append(parse_class(root, docs))

#     return result
