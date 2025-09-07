from textwrap import dedent
import re

from godocs.translation.ast import TagNode, TextNode

from godocs.translation.interpreter import BBCodeInterpreter as Interpreter

# [b]bold text[/b]
# [url=https://github.com/nadjiel]nadjiel[/url]
# [color=red]red text[/color]
# [img width=32]res://icon.svg[/img]
# [br]
# [member color]
# [operator Color.operator *]


def test_bbcode_interpreter_parse_options_maps_default_option():
    # Arrange
    text = "=https://github.com/nadjiel"

    interpreter = Interpreter()

    # Act
    options = interpreter.parse_options(text)

    # Assert
    assert len(options["list"]) == 0
    assert options["map"][''] == "https://github.com/nadjiel"


def test_bbcode_interpreter_parse_options_maps_options():
    # Arrange
    text = " width=32 height=16"

    interpreter = Interpreter()

    # Act
    options = interpreter.parse_options(text)

    # Assert
    assert len(options["list"]) == 0
    assert options["map"]["width"] == "32"
    assert options["map"]["height"] == "16"


def test_bbcode_interpreter_parse_options_lists_options():
    # Arrange
    text = " Color.operator *"

    interpreter = Interpreter()

    # Act
    options = interpreter.parse_options(text)

    # Assert
    assert options["list"][0] == "Color.operator"
    assert options["list"][1] == "*"


def test_bbcode_interpreter_parse_reference_tag_understands_annotation():
    # Arrange
    reference = "[annotation @GDScript.@rpc]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_reference_tag(reference_match)

    # Assert
    assert str(ast) == "<reference type=annotation, name=@GDScript.@rpc>"


def test_bbcode_interpreter_parse_reference_tag_understands_constant():
    # Arrange
    reference = "[constant Color.RED]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_reference_tag(reference_match)

    # Assert
    assert str(ast) == "<reference type=constant, name=Color.RED>"


def test_bbcode_interpreter_parse_reference_tag_understands_enum():
    # Arrange
    reference = "[enum Mesh.ArrayType]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_reference_tag(reference_match)

    # Assert
    assert str(ast) == "<reference type=enum, name=Mesh.ArrayType>"


def test_bbcode_interpreter_parse_reference_tag_understands_member():
    # Arrange
    reference = "[member Node2D.scale]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_reference_tag(reference_match)

    # Assert
    assert str(ast) == "<reference type=member, name=Node2D.scale>"


def test_bbcode_interpreter_parse_reference_tag_understands_method():
    # Arrange
    reference = "[method Node3D.hide]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_reference_tag(reference_match)

    # Assert
    assert str(ast) == "<reference type=method, name=Node3D.hide>"


def test_bbcode_interpreter_parse_reference_tag_understands_constructor():
    # Arrange
    reference = "[constructor Color.Color]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_reference_tag(reference_match)

    # Assert
    assert str(ast) == "<reference type=constructor, name=Color.Color>"


def test_bbcode_interpreter_parse_reference_tag_understands_operator():
    # Arrange
    reference = "[operator Color.operator *]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_reference_tag(reference_match)

    # Assert
    assert str(ast) == "<reference type=operator, name=Color.operator, symbol=*>"


def test_bbcode_interpreter_parse_reference_tag_understands_signal():
    # Arrange
    reference = "[signal Node.renamed]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_reference_tag(reference_match)

    # Assert
    assert str(ast) == "<reference type=signal, name=Node.renamed>"


def test_bbcode_interpreter_parse_reference_tag_understands_theme_item():
    # Arrange
    reference = "[theme_item Label.font]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_reference_tag(reference_match)

    # Assert
    assert str(ast) == "<reference type=theme_item, name=Label.font>"


def test_bbcode_interpreter_parse_reference_tag_understands_param():
    # Arrange
    reference = "[param size]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_reference_tag(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<code
			"size"
		>
	""").strip()


def test_bbcode_interpreter_parse_reference_tag_understands_class():
    # Arrange
    reference = "[Class]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_reference_tag(reference_match)

    # Assert
    assert str(ast) == "<reference type=class, name=Class>"


def test_bbcode_interpreter_parses_text():
    # Arrange
    text = "Hello, World!"

    interpreter = Interpreter()

    # Act
    ast = interpreter.interpret(text)

    # Assert
    assert str(ast) == dedent("""
		<root
			"Hello, World!"
		>
	""").strip()


# def test_bbcode_interpreter_parses_tag_bold():
#     # Arrange
#     text = "[b]Hello, World![/b]"

#     interpreter = Interpreter()

#     # Act
#     ast = interpreter.interpret(text)

#     print((str(ast)))
#     print(repr(dedent("""
# 		<root
# 			<bold
# 				"Hello, World!"
# 			>
# 		>
# 	""").strip()))

#     # Assert
#     assert str(ast) == dedent("""
# 		<root
# 			<bold
# 				"Hello, World!"
# 			>
# 		>
# 	""").strip()


# def test_rst_syntax_translator_translates_tag_bold():
#     # Arrange
#     text = TextNode("Hello, World!")
#     bold = TagNode("bold", [text])

#     translator = Translator()

#     # Act
#     rst = translator.translate_tag(bold)

#     # Assert
#     assert rst == "**Hello, World!**"


# def test_rst_syntax_translator_translates_tag_newline():
#     # Arrange
#     newline = TagNode("newline")

#     translator = Translator()

#     # Act
#     rst = translator.translate_tag(newline)

#     # Assert
#     assert rst == "\n"


# def test_rst_syntax_translator_translates_tag_italics():
#     # Arrange
#     text = TextNode("Hello, World!")
#     italic = TagNode("italic", [text])

#     translator = Translator()

#     # Act
#     rst = translator.translate_tag(italic)

#     # Assert
#     assert rst == "*Hello, World!*"


# def test_rst_syntax_translator_translates_tag_paragraph():
#     # Arrange
#     text = TextNode("Hello, World!")
#     paragraph = TagNode("paragraph", [text])

#     translator = Translator()

#     # Act
#     rst = translator.translate_tag(paragraph)

#     # Assert
#     assert rst == "Hello, World!"


# def test_rst_syntax_translator_translates_tag_code():
#     # Arrange
#     text = TextNode("Hello, World!")
#     code = TagNode("code", [text])

#     translator = Translator()

#     # Act
#     rst = translator.translate_tag(code)

#     # Assert
#     assert rst == "``Hello, World!``"


# def test_rst_syntax_translator_translates_tag_codeblock():
#     # Arrange
#     text = TextNode("Hello, World!")
#     codeblock = TagNode("codeblock", [text])

#     translator = Translator()

#     # Act
#     rst = translator.translate_tag(codeblock)

#     # Assert
#     assert rst == dedent("""
#     .. codeblock::

#        Hello, World!
#     """).strip()


# def test_rst_syntax_translator_translates_tag_codeblock_with_language():
#     # Arrange
#     text = TextNode("Hello, World!")
#     codeblock = TagNode("codeblock", [text], {"language": "python"})

#     translator = Translator()

#     # Act
#     rst = translator.translate_tag(codeblock)

#     # Assert
#     assert rst == dedent("""
#     .. codeblock:: python

#        Hello, World!
#     """).strip()


# def test_rst_syntax_translator_translates_tag_link():
#     # Arrange
#     text = TextNode("Godocs")
#     link = TagNode("link", [text], {
#                    "url": "https://github.com/godocs-godot/godocs"})

#     translator = Translator()

#     # Act
#     rst = translator.translate_tag(link)

#     # Assert
#     assert rst == "Godocs <https://github.com/godocs-godot/godocs>_"


# def test_rst_syntax_translator_translates_reference():
#     # Arrange
#     text = TextNode("Godocs")
#     link = TagNode("reference", [text], {"name": "RSTSyntaxTranslator"})

#     translator = Translator()

#     # Act
#     rst = translator.translate_tag(link)

#     # Assert
#     assert rst == ":ref:`RSTSyntaxTranslator <RSTSyntaxTranslator>`"
