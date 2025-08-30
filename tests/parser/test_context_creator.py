import pytest
import xml.etree.ElementTree as ET

from godocs.parser.context_creator import get_class_node

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
