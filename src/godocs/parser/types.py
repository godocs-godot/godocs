import xml.etree.ElementTree as ET
from typing import TypedDict


class Property(TypedDict):
    name: str
    type: str
    default: str
    description: str


class Method(TypedDict):
    name: str
    type: str
    args: list[Property]
    description: str


type XMLNode = ET.Element[str]

type XMLDoc = ET.ElementTree[XMLNode]
