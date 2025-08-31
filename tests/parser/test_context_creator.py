import pytest
import xml.etree.ElementTree as ET

from godocs.parser.context_creator import (
    get_class_node,
    parse_inheritage,
    parse_property,
    parse_method,
    parse_signal,
    parse_constant,
    parse_enum,
    parse_theme_item,
    parse_properties,
    parse_methods,
    parse_signals,
)

from godocs.parser.types import XMLDoc


def test_get_class_node_finds_class():
    # Arrange
    docs: list[XMLDoc] = [
        ET.ElementTree(ET.fromstring('<class name="A"></class>')),
        ET.ElementTree(ET.fromstring('<class name="B"></class>'))
    ]

    # Act
    class_node = get_class_node("B", docs)

    # Assert
    assert class_node is not None
    assert class_node.attrib["name"] == "B"


def test_get_class_node_returns_none():
    # Arrange
    docs: list[XMLDoc] = [
        ET.ElementTree(ET.fromstring('<class name="A"></class>')),
        ET.ElementTree(ET.fromstring('<class name="B"></class>'))
    ]

    # Act
    class_node = get_class_node("C", docs)

    # Assert
    assert class_node is None


def test_parse_inheritage_succeds():
    # Arrange
    class_c = ET.fromstring('<class name="C" inherits="A"></class>')
    docs: list[XMLDoc] = [
        ET.ElementTree(ET.fromstring('<class name="A" inherits="B"></class>')),
        ET.ElementTree(ET.fromstring('<class name="B"></class>')),
        ET.ElementTree(class_c),
    ]

    # Act
    inheritage = parse_inheritage(class_c, docs)

    # Assert
    assert inheritage[0] == "A"
    assert inheritage[1] == "B"


def test_parse_inheritage_unexisting():
    # Arrange
    class_c = ET.fromstring('<class name="C"></class>')
    docs: list[XMLDoc] = [
        ET.ElementTree(ET.fromstring('<class name="A"></class>')),
        ET.ElementTree(ET.fromstring('<class name="B"></class>')),
        ET.ElementTree(class_c),
    ]

    # Act
    inheritage = parse_inheritage(class_c, docs)

    # Assert
    assert len(inheritage) == 0


def test_parse_property_succeds():
    # Arrange
    property = ET.fromstring("""
        <member name="color" type="Color" setter="set_color" getter="get_color" default="null">
          Description
        </member>
    """)

    # Act
    result = parse_property(property)

    # Assert
    assert result["name"] == "color"
    assert result["type"] == "Color"
    assert result["default"] == "null"
    assert result["description"] == "Description"


def test_parse_method_succeds():
    # Arrange
    method = ET.fromstring("""
        <method name="add">
          <return type="int" />
          <param index="0" name="num1" type="int" />
          <param index="1" name="num2" type="int" />
          <description>
            Description
          </description>
        </method>
    """)

    # Act
    result = parse_method(method)

    # Assert
    assert result["name"] == "add"
    assert result["type"] == "int"
    assert result["args"][0]["name"] == "num1"
    assert result["args"][0]["type"] == "int"
    assert result["args"][0]["default"] == ""
    assert result["args"][0]["description"] == ""
    assert result["args"][1]["name"] == "num2"
    assert result["args"][1]["type"] == "int"
    assert result["args"][1]["default"] == ""
    assert result["args"][1]["description"] == ""
    assert result["description"] == "Description"


def test_parse_signal_succeds():
    # Arrange
    signal = ET.fromstring("""
        <signal name="swapped_positions">
          <param index="0" name="prev" type="int" />
          <param index="1" name="next" type="int" />
          <description>
            Description
          </description>
	    </signal>
    """)

    # Act
    result = parse_signal(signal)

    # Assert
    assert result["name"] == "swapped_positions"
    assert result["args"][0]["name"] == "prev"
    assert result["args"][0]["type"] == "int"
    assert result["args"][0]["default"] == ""
    assert result["args"][0]["description"] == ""
    assert result["args"][1]["name"] == "next"
    assert result["args"][1]["type"] == "int"
    assert result["args"][1]["default"] == ""
    assert result["args"][1]["description"] == ""
    assert result["description"] == "Description"


def test_parse_constant_succeds():
    # Arrange
    constant = ET.fromstring("""
        <constant name="PI" value="3.14">
          The value of PI.
        </constant>
    """)

    # Act
    result = parse_constant(constant)

    # Assert
    assert result["name"] == "PI"
    assert result["value"] == "3.14"
    assert result["description"] == "The value of PI."


def test_parse_enum_succeds():
    # Arrange
    values = [
        ET.fromstring("""
            <constant name="ADDITION" value="0" enum="Operation">
              Operation of adding two numbers.
            </constant>
        """),
        ET.fromstring("""
            <constant name="SUBTRACTION" value="1" enum="Operation">
              Operation of subtracting two numbers.
            </constant>
        """),
    ]

    # Act
    result = parse_enum("Operation", values)

    # Assert
    assert result["name"] == "Operation"
    assert result["values"][0]["name"] == "ADDITION"
    assert result["values"][0]["value"] == "0"
    assert result["values"][0]["description"] == "Operation of adding two numbers."
    assert result["values"][1]["name"] == "SUBTRACTION"
    assert result["values"][1]["value"] == "1"
    assert result["values"][1]["description"] == "Operation of subtracting two numbers."
    assert result["description"] == ""


def test_parse_theme_item_succeds():
    # Arrange
    theme_item = ET.fromstring("""
        <theme_item name="font_color" data_type="color" type="Color" default="Color(0.875, 0.875, 0.875, 1)">
		  Default text [Color] of the [Button].
		</theme_item>
    """)

    # Act
    result = parse_theme_item(theme_item)

    # Assert
    assert result["name"] == "font_color"
    assert result["data_type"] == "color"
    assert result["type"] == "Color"
    assert result["default"] == "Color(0.875, 0.875, 0.875, 1)"
    assert result["description"] == "Default text [Color] of the [Button]."


def test_parse_properties_succeds():
    # Arrange
    properties = ET.fromstring("""
        <members>
          <member name="color" type="Color" setter="set_color" getter="get_color" default="null">
            A thinga with color and name.
          </member>
          <member name="name" type="String" setter="set_name" getter="get_name" default="null">
            The name of the thinga.
          </member>
        </members>
    """)

    # Act
    result = parse_properties(properties)

    # Assert
    assert result[0]["name"] == "color"
    assert result[0]["type"] == "Color"
    assert result[0]["default"] == "null"
    assert result[0]["description"] == "A thinga with color and name."
    assert result[1]["name"] == "name"
    assert result[1]["type"] == "String"
    assert result[1]["default"] == "null"
    assert result[1]["description"] == "The name of the thinga."


def test_parse_methods_succeeds():
    # Arrange
    methods = ET.fromstring("""
        <methods>
          <method name="add">
            <return type="int" />
            <param index="0" name="num1" type="int" />
            <param index="1" name="num2" type="int" />
            <description>
              Adds two numbers.
            </description>
          </method>
          <method name="subtract">
            <return type="int" />
            <param index="0" name="num1" type="int" />
            <param index="1" name="num2" type="int" />
            <description>
              Subtracts the second number from the first.
            </description>
          </method>
        </methods>
    """)

    # Act
    result = parse_methods(methods)

    # Assert
    assert result[0]["name"] == "add"
    assert result[0]["type"] == "int"
    assert result[0]["description"] == "Adds two numbers."
    assert len(result[0]["args"]) == 2
    assert result[0]["args"][0]["name"] == "num1"
    assert result[0]["args"][0]["type"] == "int"
    assert result[0]["args"][1]["name"] == "num2"
    assert result[0]["args"][1]["type"] == "int"

    assert result[1]["name"] == "subtract"
    assert result[1]["type"] == "int"
    assert result[1]["description"] == "Subtracts the second number from the first."
    assert len(result[1]["args"]) == 2
    assert result[1]["args"][0]["name"] == "num1"
    assert result[1]["args"][0]["type"] == "int"
    assert result[1]["args"][1]["name"] == "num2"
    assert result[1]["args"][1]["type"] == "int"


def test_parse_signals_succeeds():
    # Arrange
    signals = ET.fromstring("""
        <signals>
          <signal name="damaged">
            <param index="0" name="amount" type="float" />
            <description>
              Emitted when someone gets damaged.
            </description>
          </signal>
          <signal name="healed">
            <param index="0" name="amount" type="float" />
            <description>
              Emitted when someone gets healed.
            </description>
          </signal>
        </signals>
    """)

    # Act
    result = parse_signals(signals)

    # Assert
    assert result[0]["name"] == "damaged"
    assert result[0]["description"] == "Emitted when someone gets damaged."
    assert len(result[0]["args"]) == 1
    assert result[0]["args"][0]["name"] == "amount"
    assert result[0]["args"][0]["type"] == "float"
    assert result[0]["args"][0]["default"] == ""
    assert result[0]["args"][0]["description"] == ""

    assert result[1]["name"] == "healed"
    assert result[1]["description"] == "Emitted when someone gets healed."
    assert len(result[1]["args"]) == 1
    assert result[1]["args"][0]["name"] == "amount"
    assert result[1]["args"][0]["type"] == "float"
    assert result[1]["args"][0]["default"] == ""
    assert result[1]["args"][0]["description"] == ""


# def test_parse_file_invalid_xml(tmp_path: Path):
#     # Arrange
#     file = tmp_path / "test.xml"
#     file.write_text("<root><child>value</child>")

#     # Assert
#     with pytest.raises(ET.ParseError):
#         parse_file(file)


# def test_parse_file_missing_file(tmp_path: Path):
#     # Arrange
#     file = tmp_path / "test.xml"

#     # Assert
#     with pytest.raises(FileNotFoundError):
#         parse_file(file)


# def test_parse_folder_multiple_files(tmp_path: Path):
#     # Arrange
#     xml1 = tmp_path / "a.xml"
#     xml2 = tmp_path / "b.xml"
#     not_xml = tmp_path / "c.txt"

#     xml1.write_text("<root><child>A</child></root>")
#     xml2.write_text("<root><child>B</child></root>")
#     not_xml.write_text("Not XML")  # should be ignored

#     # Act
#     trees = parse_folder(tmp_path)

#     # Assert
#     assert len(trees) == 2
#     assert {t.getroot().find("child").text for t in trees} == {  # type: ignore
#         "A", "B"}


# def test_parse_folder_not_a_directory(tmp_path: Path):
#     # Arrange
#     file = tmp_path / "test.xml"
#     file.write_text("<root/>")

#     # Assert
#     with pytest.raises(NotADirectoryError):
#         parse_folder(file)


# def test_parse_with_file(tmp_path: Path):
#     # Arrange
#     file = tmp_path / "test.xml"
#     file.write_text("<root/>")

#     # Act
#     trees = parse(file)

#     # Assert
#     assert len(trees) == 1
#     assert trees[0].getroot().tag == "root"


# def test_parse_with_folder(tmp_path: Path):
#     # Arrange
#     xml_file = tmp_path / "test.xml"
#     xml_file.write_text("<root><child/></root>")

#     # Act
#     trees = parse(tmp_path)

#     # Assert
#     assert isinstance(trees, list)
#     assert len(trees) == 1
#     assert trees[0].getroot().tag == "root"
