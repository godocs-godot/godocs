import xml.etree.ElementTree as ET
from typing import TypedDict


class Property(TypedDict):
    name: str
    type: str
    default: str
    description: str


class Constant(TypedDict):
    name: str
    value: str
    description: str


class Method(TypedDict):
    name: str
    type: str
    args: list[Property]
    description: str


class Signal(TypedDict):
    name: str
    args: list[Property]
    description: str


class Enum(TypedDict):
    name: str
    values: list[Constant]
    description: str


type XMLNode = ET.Element[str]

type XMLDoc = ET.ElementTree[XMLNode]
