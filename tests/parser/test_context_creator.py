import xml.etree.ElementTree as ET

from godocs.parser.context_creator import (
    get_class_node,
    parse_inheritage,
    parse_property,
    parse_method,
    parse_signal,
    parse_constant,
    parse_enum,
    parse_theme_item,
    parse_properties,
    parse_methods,
    parse_signals,
    parse_constants,
    parse_enums,
    parse_theme_items,
    parse_class,
)

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


def test_parse_constant_succeds():
    # Arrange
    constant = ET.fromstring("""
        <constant name="PI" value="3.14">
          The value of PI.
        </constant>
    """)

    # Act
    result = parse_constant(constant)

    # Assert
    assert result["name"] == "PI"
    assert result["value"] == "3.14"
    assert result["description"] == "The value of PI."


def test_parse_enum_succeds():
    # Arrange
    values = [
        ET.fromstring("""
            <constant name="ADDITION" value="0" enum="Operation">
              Operation of adding two numbers.
            </constant>
        """),
        ET.fromstring("""
            <constant name="SUBTRACTION" value="1" enum="Operation">
              Operation of subtracting two numbers.
            </constant>
        """),
    ]

    # Act
    result = parse_enum("Operation", values)

    # Assert
    assert result["name"] == "Operation"
    assert result["values"][0]["name"] == "ADDITION"
    assert result["values"][0]["value"] == "0"
    assert result["values"][0]["description"] == "Operation of adding two numbers."
    assert result["values"][1]["name"] == "SUBTRACTION"
    assert result["values"][1]["value"] == "1"
    assert result["values"][1]["description"] == "Operation of subtracting two numbers."
    assert result["description"] == ""


def test_parse_theme_item_succeds():
    # Arrange
    theme_item = ET.fromstring("""
        <theme_item name="font_color" data_type="color" type="Color" default="Color(0.875, 0.875, 0.875, 1)">
		  Default text [Color] of the [Button].
		</theme_item>
    """)

    # Act
    result = parse_theme_item(theme_item)

    # Assert
    assert result["name"] == "font_color"
    assert result["data_type"] == "color"
    assert result["type"] == "Color"
    assert result["default"] == "Color(0.875, 0.875, 0.875, 1)"
    assert result["description"] == "Default text [Color] of the [Button]."


def test_parse_properties_succeds():
    # Arrange
    properties = ET.fromstring("""
        <members>
          <member name="color" type="Color" setter="set_color" getter="get_color" default="null">
            A thinga with color and name.
          </member>
          <member name="name" type="String" setter="set_name" getter="get_name" default="null">
            The name of the thinga.
          </member>
        </members>
    """)

    # Act
    result = parse_properties(properties)

    # Assert
    assert result[0]["name"] == "color"
    assert result[0]["type"] == "Color"
    assert result[0]["default"] == "null"
    assert result[0]["description"] == "A thinga with color and name."
    assert result[1]["name"] == "name"
    assert result[1]["type"] == "String"
    assert result[1]["default"] == "null"
    assert result[1]["description"] == "The name of the thinga."


def test_parse_methods_succeeds():
    # Arrange
    methods = ET.fromstring("""
        <methods>
          <method name="add">
            <return type="int" />
            <param index="0" name="num1" type="int" />
            <param index="1" name="num2" type="int" />
            <description>
              Adds two numbers.
            </description>
          </method>
          <method name="subtract">
            <return type="int" />
            <param index="0" name="num1" type="int" />
            <param index="1" name="num2" type="int" />
            <description>
              Subtracts the second number from the first.
            </description>
          </method>
        </methods>
    """)

    # Act
    result = parse_methods(methods)

    # Assert
    assert result[0]["name"] == "add"
    assert result[0]["type"] == "int"
    assert result[0]["description"] == "Adds two numbers."
    assert len(result[0]["args"]) == 2
    assert result[0]["args"][0]["name"] == "num1"
    assert result[0]["args"][0]["type"] == "int"
    assert result[0]["args"][1]["name"] == "num2"
    assert result[0]["args"][1]["type"] == "int"

    assert result[1]["name"] == "subtract"
    assert result[1]["type"] == "int"
    assert result[1]["description"] == "Subtracts the second number from the first."
    assert len(result[1]["args"]) == 2
    assert result[1]["args"][0]["name"] == "num1"
    assert result[1]["args"][0]["type"] == "int"
    assert result[1]["args"][1]["name"] == "num2"
    assert result[1]["args"][1]["type"] == "int"


def test_parse_signals_succeeds():
    # Arrange
    signals = ET.fromstring("""
        <signals>
          <signal name="damaged">
            <param index="0" name="amount" type="float" />
            <description>
              Emitted when someone gets damaged.
            </description>
          </signal>
          <signal name="healed">
            <param index="0" name="amount" type="float" />
            <description>
              Emitted when someone gets healed.
            </description>
          </signal>
        </signals>
    """)

    # Act
    result = parse_signals(signals)

    # Assert
    assert result[0]["name"] == "damaged"
    assert result[0]["description"] == "Emitted when someone gets damaged."
    assert len(result[0]["args"]) == 1
    assert result[0]["args"][0]["name"] == "amount"
    assert result[0]["args"][0]["type"] == "float"
    assert result[0]["args"][0]["default"] == ""
    assert result[0]["args"][0]["description"] == ""

    assert result[1]["name"] == "healed"
    assert result[1]["description"] == "Emitted when someone gets healed."
    assert len(result[1]["args"]) == 1
    assert result[1]["args"][0]["name"] == "amount"
    assert result[1]["args"][0]["type"] == "float"
    assert result[1]["args"][0]["default"] == ""
    assert result[1]["args"][0]["description"] == ""


def test_parse_constants_succeeds():
    # Arrange
    constants = ET.fromstring("""
        <constants>
          <constant name="PI" value="3.14">
            The value of PI.
          </constant>
          <constant name="E" value="2.71">
            The value of Euler's number.
          </constant>
        </constants>
    """)

    # Act
    result = parse_constants(constants)

    # Assert
    assert result[0]["name"] == "PI"
    assert result[0]["value"] == "3.14"
    assert result[0]["description"] == "The value of PI."
    assert result[1]["name"] == "E"
    assert result[1]["value"] == "2.71"
    assert result[1]["description"] == "The value of Euler's number."


def test_parse_constants_ignores_enums():
    # Arrange
    constants = ET.fromstring("""
        <constants>
          <constant name="PI" value="3.14">
            The value of PI.
          </constant>
          <constant name="E" value="2.71">
            The value of Euler's number.
          </constant>
          <constant name="ADDITION" value="0" enum="OPERATIONS">
            The addition operation.
          </constant>
          <constant name="SUBTRACTION" value="1" enum="OPERATIONS">
            The subtraction operation.
          </constant>
        </constants>
    """)

    # Act
    result = parse_constants(constants)

    # Assert
    assert len(result) == 2
    assert result[0]["name"] == "PI"
    assert result[1]["name"] == "E"


def test_parse_enums_ignores_constants():
    # Arrange
    constants = ET.fromstring("""
        <constants>
          <constant name="PI" value="3.14">
            The value of PI.
          </constant>
          <constant name="E" value="2.71">
            The value of Euler's number.
          </constant>
          <constant name="ADDITION" value="0" enum="Operation">
            The addition operation.
          </constant>
          <constant name="SUBTRACTION" value="1" enum="Operation">
            The subtraction operation.
          </constant>
        </constants>
    """)

    # Act
    result = parse_enums(constants)

    # Assert
    assert len(result) == 1
    assert result[0]["name"] == "Operation"
    assert len(result[0]["values"]) == 2
    assert result[0]["values"][0]["name"] == "ADDITION"
    assert result[0]["values"][0]["value"] == "0"
    assert result[0]["values"][0]["description"] == "The addition operation."
    assert result[0]["values"][1]["name"] == "SUBTRACTION"
    assert result[0]["values"][1]["value"] == "1"
    assert result[0]["values"][1]["description"] == "The subtraction operation."


def test_parse_theme_items_succeeds():
    # Arrange
    theme_items = ET.fromstring("""
        <theme_items>
          <theme_item name="font_color" data_type="color" type="Color" default="black">
            The default font color.
          </theme_item>
          <theme_item name="font_size" data_type="int" type="int" default="14">
            The default font size.
          </theme_item>
        </theme_items>
    """)

    # Act
    result = parse_theme_items(theme_items)

    # Assert
    assert result[0]["name"] == "font_color"
    assert result[0]["data_type"] == "color"
    assert result[0]["type"] == "Color"
    assert result[0]["default"] == "black"
    assert result[0]["description"] == "The default font color."

    assert result[1]["name"] == "font_size"
    assert result[1]["data_type"] == "int"
    assert result[1]["type"] == "int"
    assert result[1]["default"] == "14"
    assert result[1]["description"] == "The default font size."


def test_parse_class_succeds():
    # Arrange
    class_xml: XMLDoc = ET.ElementTree(ET.fromstring("""
        <class name="FakeClass" inherits="Reference" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/godotengine/godot/master/doc/class.xsd">
          <brief_description>
            A fake class for parser testing.
          </brief_description>
          <description>
            This class is only used to test the XML parser for different node types.
          </description>
          <tutorials>
          </tutorials>
  
          <methods>
            <method name="do_something">
            <return type="void" />
            <param index="0" name="value" type="int" />
            <description>
              Does something with a value.
            </description>
            </method>
          </methods>
  
          <members>
            <member name="enabled" type="bool" default="true">
            Whether the class is enabled.
            </member>
          </members>
  
          <signals>
            <signal name="changed">
            <param index="0" name="what" type="String" />
            <description>
              Emitted when something changes.
            </description>
            </signal>
          </signals>
  
          <constants>
            <constant name="VERSION" value="1">
              Version number of this class.
            </constant>
            <constant name="STATE" value="0" enum="StateMachine">
              Enum member for class state.
            </constant>
          </constants>
  
          <theme_items>
            <theme_item name="font_color" data_type="color" type="Color" default="black">
              The default font color.
            </theme_item>
          </theme_items>
        </class>
    """))

    # Act
    result = parse_class(class_xml.getroot(), [class_xml])

    assert result["name"] == "FakeClass"
    assert result["brief_description"] == "A fake class for parser testing."
    assert result["description"] == "This class is only used to test the XML parser for different node types."
    assert len(result["methods"]) == 1
    assert result["methods"][0]["name"] == "do_something"
    assert len(result["properties"]) == 1
    assert result["properties"][0]["name"] == "enabled"
    assert len(result["signals"]) == 1
    assert result["signals"][0]["name"] == "changed"
    assert len(result["constants"]) == 1
    assert result["constants"][0]["name"] == "VERSION"
    assert len(result["enums"]) == 1
    assert result["enums"][0]["name"] == "StateMachine"
    assert len(result["theme_items"]) == 1
    assert result["theme_items"][0]["name"] == "font_color"
