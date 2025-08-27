import pytest
from pathlib import Path
import xml.etree.ElementTree as ET

from godocs.parser.xml_parser import parse_file, parse_folder, parse


def test_parse_file_valid_xml(tmp_path: Path):
    file = tmp_path / "test.xml"
    file.write_text("<root><child>value</child></root>")

    tree = parse_file(file)
    root = tree.getroot()

    assert root.tag == "root"
    assert root.find("child").text == "value"


def test_parse_file_invalid_xml(tmp_path: Path):
    file = tmp_path / "bad.xml"
    file.write_text("<root><child></root>")  # malformed XML

    with pytest.raises(ET.ParseError):
        parse_file(file)


def test_parse_file_missing_file(tmp_path: Path):
    file = tmp_path / "does_not_exist.xml"
    with pytest.raises(FileNotFoundError):
        parse_file(file)


def test_parse_folder_multiple_files(tmp_path: Path):
    xml1 = tmp_path / "a.xml"
    xml2 = tmp_path / "b.xml"
    not_xml = tmp_path / "c.txt"

    xml1.write_text("<root><child>A</child></root>")
    xml2.write_text("<root><child>B</child></root>")
    not_xml.write_text("Not XML")  # should be ignored

    trees = parse_folder(tmp_path)

    assert len(trees) == 2
    assert {t.getroot().find("child").text for t in trees} == {"A", "B"}


def test_parse_folder_not_a_directory(tmp_path: Path):
    file = tmp_path / "test.xml"
    file.write_text("<root/>")

    with pytest.raises(NotADirectoryError):
        # force this by calling parse_folder on a file instead of a folder
        parse_folder(file)


def test_parse_with_file(tmp_path: Path):
    file = tmp_path / "test.xml"
    file.write_text("<root/>")

    trees = parse(file)

    assert isinstance(trees, list)
    assert len(trees) == 1
    assert trees[0].getroot().tag == "root"


def test_parse_with_folder(tmp_path: Path):
    xml_file = tmp_path / "test.xml"
    xml_file.write_text("<root><child/></root>")

    trees = parse(tmp_path)

    assert isinstance(trees, list)
    assert len(trees) == 1
    assert trees[0].getroot().tag == "root"
