from textwrap import dedent
import re

from godocs.translation.interpreter import BBCodeInterpreter as Interpreter


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


def test_bbcode_interpreter_parse_tag_understands_line_break():
    # Arrange
    reference = "[br]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_tag(reference_match)

    # Assert
    assert str(ast) == "<newline>"


def test_bbcode_interpreter_parse_tag_understands_left_square_bracket():
    # Arrange
    reference = "[lb]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_tag(reference_match)

    # Assert
    assert str(ast) == '"["'


def test_bbcode_interpreter_parse_tag_understands_right_square_bracket():
    # Arrange
    reference = "[rb]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_tag(reference_match)

    # Assert
    assert str(ast) == '"]"'


# def test_bbcode_interpreter_parse_element_understands_paragraph():
#     # Arrange
#     reference = "[p]text[/p]"

#     interpreter = Interpreter()

#     reference_match = re.match(interpreter.el_regex, reference)

#     assert reference_match is not None

#     # Act
#     ast = interpreter.parse_element(reference_match)

#     # Assert
#     assert str(ast) == dedent("""
# 		<paragraph
# 			"text"
# 		>
# 	""").strip()


def test_bbcode_interpreter_parse_element_understands_bold():
    # Arrange
    reference = "[b]text[/b]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<bold
			"text"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_italic():
    # Arrange
    reference = "[i]text[/i]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<italic
			"text"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_underline():
    # Arrange
    reference = "[u]text[/u]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<underline
			"text"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_strikethrough():
    # Arrange
    reference = "[s]text[/s]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<strikethrough
			"text"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_color():
    # Arrange
    reference = "[color=red]text[/color]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<color value=red
			"text"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_font():
    # Arrange
    reference = "[font=res://mono.ttf]text[/font]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<font url=res://mono.ttf
			"text"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_image():
    # Arrange
    reference = "[img width=32]text[/img]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<image width=32
			"text"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_link_without_url():
    # Arrange
    reference = "[url]https://github.com/nadjiel[/url]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<link url=https://github.com/nadjiel
			"https://github.com/nadjiel"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_link():
    # Arrange
    reference = "[url=https://github.com/nadjiel]nadjiel[/url]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<link url=https://github.com/nadjiel
			"nadjiel"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_center():
    # Arrange
    reference = "[center]text[/center]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<alignment x=center
			"text"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_keyboard():
    # Arrange
    reference = "[kbd]Ctrl + C[/kbd]"

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<keyboard
			"Ctrl + C"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_code():
    # Arrange
    reference = '[code]print("Hello, world!")[/code]'

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<code
			"print("Hello, world!")"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_codeblock_without_language():
    # Arrange
    reference = '[codeblock]print("Hello, world!")[/codeblock]'

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<codeblock language=
			"print("Hello, world!")"
		>
	""").strip()


def test_bbcode_interpreter_parse_element_understands_codeblock():
    # Arrange
    reference = '[codeblock lang=gdscript]print("Hello, world!")[/codeblock]'

    interpreter = Interpreter()

    reference_match = re.match(interpreter.el_regex, reference)

    assert reference_match is not None

    # Act
    ast = interpreter.parse_element(reference_match)

    # Assert
    assert str(ast) == dedent("""
		<codeblock language=gdscript
			"print("Hello, world!")"
		>
	""").strip()


def test_bbcode_interpreter_interpret_understands_simple_text():
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


def test_bbcode_interpreter_interpret_understands_empty_string():
    # Arrange
    text = ""

    interpreter = Interpreter()

    # Act
    ast = interpreter.interpret(text)

    assert str(ast) == dedent("""
		<root
			""
		>
	""").strip()


def test_bbcode_interpreter_interpret_understands_bold():
    # Arrange
    text = "[b]Hello, World![/b]"

    interpreter = Interpreter()

    # Act
    ast = interpreter.interpret(text)

    assert str(ast) == dedent("""
		<root
			<bold
				"Hello, World!"
			>
		>
	""").strip()


def test_bbcode_interpreter_interpret_understands_sibling_tags():
    # Arrange
    text = "Start Text [b]Bold[/b] [i]Italic[/i] End Text"

    interpreter = Interpreter()

    # Act
    ast = interpreter.interpret(text)

    assert str(ast) == dedent("""
		<root
			"Start Text ",
			<bold
				"Bold"
			>,
			" ",
			<italic
				"Italic"
			>,
			" End Text"
		>
	""").strip()


def test_bbcode_interpreter_interpret_understands_nested_tags():
    # Arrange
    text = "[b]Wrapper [i]Inner Wrapper [u]Inner Text[/u] Text[/i] Text[/b]"

    interpreter = Interpreter()

    # Act
    ast = interpreter.interpret(text)

    assert str(ast) == dedent("""
		<root
			<bold
				"Wrapper ",
				<italic
					"Inner Wrapper ",
					<underline
						"Inner Text"
					>,
					" Text"
				>,
				" Text"
			>
		>
	""").strip()
