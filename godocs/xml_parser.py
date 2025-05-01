from pathlib import Path
import xml.etree.ElementTree as ET

def parse_file(path: str | Path) -> ET.ElementTree:
  if isinstance(path, str):
    path = Path(path)
  
  tree = ET.parse(path)

  return tree

def parse(path: str | Path) -> list[ET.ElementTree]:
  if isinstance(path, str):
    path = Path(path)

  result: list[ET.ElementTree] = []

  if path.is_file():
    result.append(parse_file(path))

    return result

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
