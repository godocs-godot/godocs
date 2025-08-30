import xml.etree.ElementTree as ET

type XMLNode = ET.Element[str]

type XMLDoc = ET.ElementTree[XMLNode]
