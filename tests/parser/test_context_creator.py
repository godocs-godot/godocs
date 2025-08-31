import pytest
import xml.etree.ElementTree as ET

from godocs.parser.context_creator import get_class_node, parse_inheritage, parse_property, parse_method, parse_signal

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
