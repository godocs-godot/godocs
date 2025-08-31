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


class ThemeItem(TypedDict):
    name: str
    data_type: str
    type: str
    default: str
    description: str


class Class(TypedDict):
    name: str
    inheritage: list[str]
    brief_description: str
    description: str
    properties: list[Property]
    methods: list[Method]
    signals: list[Signal]
    constants: list[Constant]
    enums: list[Enum]
    theme_items: list[ThemeItem]


type XMLNode = ET.Element[str]

type XMLDoc = ET.ElementTree[XMLNode]
