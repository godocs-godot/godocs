from pathlib import Path
import xml.etree.ElementTree as ET

def parse_file(path: str | Path) -> ET.ElementTree:
  """
  Parses an XML file from a given path and returns an ElementTree object.

  Args:
    path (str or pathlib.Path): Path to the XML file.

  Returns:
    xml.etree.ElementTree.ElementTree: Parsed ElementTree containing the XML data.
  
  Raises:
      FileNotFoundError: If the file at the given path does not exist.
      xml.etree.ElementTree.ParseError: If the file is not a valid XML document.
  """

  if isinstance(path, str):
    path = Path(path)
  
  tree = ET.parse(path)

  return tree

def parse_folder(path: str | Path) -> list[ET.ElementTree]:
  """
  Parses all XML files from a given path and returns a list with ElementTree objects.

  Args:
    path (str or pathlib.Path): Path to the folder containing XML files.

  Returns:
    list[xml.etree.ElementTree.ElementTree]: List with the parsed ElementTrees containing the XML data.
  
  Raises:
      NotADirectoryError: If the path doesn't point to a directory.
  """
  if isinstance(path, str):
    path = Path(path)

  result: list[ET.ElementTree] = []

  for subpath in path.iterdir():
    if subpath.is_dir():
      continue

    data = {}

    try:
      data = parse_file(subpath)
    except ET.ParseError as e:
      continue
    
    result.append(data)

  return result

def parse(path: str | Path) -> list[ET.ElementTree]:
  """
  Parses one or more XML files from a given path.

  If the path points to a file, parses that file.
  If the path points to a directory, parses all XML files in the directory.
  Returns a list of parsed ElementTree objects.

  Args:
    path (str or pathlib.Path): Path to an XML file or a directory containing XML files.

  Returns:
    list[xml.etree.ElementTree.ElementTree]: A list of ElementTree objects parsed from the XML files.
  
  Raises:
      FileNotFoundError: If the file at the given path does not exist.
      xml.etree.ElementTree.ParseError: If the file is not a valid XML document.
  """

  if isinstance(path, str):
    path = Path(path)

  if path.is_file():
    return [ parse_file(path) ]
  else:
    return parse_folder(path)
