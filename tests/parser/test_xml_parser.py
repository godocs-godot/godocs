import pytest
from pathlib import Path
import xml.etree.ElementTree as ET

from godocs.parser.xml_parser import parse_file, parse_folder, parse


def test_parse_file_valid_xml(tmp_path: Path):
    # Arrange
    file = tmp_path / "test.xml"
    file.write_text("<root><child>value</child></root>")

    # Act
    tree = parse_file(file)
    root = tree.getroot()

    # Assert
    assert root.tag == "root"
    assert root.find("child").text == "value"  # type: ignore


def test_parse_file_invalid_xml(tmp_path: Path):
    # Arrange
    file = tmp_path / "test.xml"
    file.write_text("<root><child>value</child>")

    # Assert
    with pytest.raises(ET.ParseError):
        parse_file(file)


def test_parse_file_missing_file(tmp_path: Path):
    # Arrange
    file = tmp_path / "test.xml"

    # Assert
    with pytest.raises(FileNotFoundError):
        parse_file(file)


def test_parse_folder_multiple_files(tmp_path: Path):
    # Arrange
    xml1 = tmp_path / "a.xml"
    xml2 = tmp_path / "b.xml"
    not_xml = tmp_path / "c.txt"

    xml1.write_text("<root><child>A</child></root>")
    xml2.write_text("<root><child>B</child></root>")
    not_xml.write_text("Not XML")  # should be ignored

    # Act
    trees = parse_folder(tmp_path)

    # Assert
    assert len(trees) == 2
    assert {t.getroot().find("child").text for t in trees} == {  # type: ignore
        "A", "B"}


def test_parse_folder_not_a_directory(tmp_path: Path):
    # Arrange
    file = tmp_path / "test.xml"
    file.write_text("<root/>")

    # Assert
    with pytest.raises(NotADirectoryError):
        parse_folder(file)


def test_parse_with_file(tmp_path: Path):
    # Arrange
    file = tmp_path / "test.xml"
    file.write_text("<root/>")

    # Act
    trees = parse(file)

    # Assert
    assert len(trees) == 1
    assert trees[0].getroot().tag == "root"


def test_parse_with_folder(tmp_path: Path):
    # Arrange
    xml_file = tmp_path / "test.xml"
    xml_file.write_text("<root><child/></root>")

    # Act
    trees = parse(tmp_path)

    # Assert
    assert isinstance(trees, list)
    assert len(trees) == 1
    assert trees[0].getroot().tag == "root"
