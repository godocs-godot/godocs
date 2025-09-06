from textwrap import dedent

from godocs.translation.ast import TagNode, TextNode

from godocs.translation.translator import RSTSyntaxTranslator as Translator


def test_rst_syntax_translator_translates_text():
    # Arrange
    text = TextNode("Hello, World!")
    # root = TagNode("root", [text])

    translator = Translator()

    # Act
    rst = translator.translate_text(text)

    # Assert
    assert rst == "Hello, World!"


def test_rst_syntax_translator_translates_tag_root():
    # Arrange
    text = TextNode("Hello, World!")
    root = TagNode("root", [text])

    translator = Translator()

    # Act
    rst = translator.translate_tag(root)

    # Assert
    assert rst == "Hello, World!"


def test_rst_syntax_translator_translates_tag_bold():
    # Arrange
    text = TextNode("Hello, World!")
    bold = TagNode("bold", [text])

    translator = Translator()

    # Act
    rst = translator.translate_tag(bold)

    # Assert
    assert rst == "**Hello, World!**"


def test_rst_syntax_translator_translates_tag_newline():
    # Arrange
    newline = TagNode("newline")

    translator = Translator()

    # Act
    rst = translator.translate_tag(newline)

    # Assert
    assert rst == "\n"


def test_rst_syntax_translator_translates_tag_italics():
    # Arrange
    text = TextNode("Hello, World!")
    italic = TagNode("italic", [text])

    translator = Translator()

    # Act
    rst = translator.translate_tag(italic)

    # Assert
    assert rst == "*Hello, World!*"


def test_rst_syntax_translator_translates_tag_paragraph():
    # Arrange
    text = TextNode("Hello, World!")
    paragraph = TagNode("paragraph", [text])

    translator = Translator()

    # Act
    rst = translator.translate_tag(paragraph)

    # Assert
    assert rst == "Hello, World!"


def test_rst_syntax_translator_translates_tag_code():
    # Arrange
    text = TextNode("Hello, World!")
    code = TagNode("code", [text])

    translator = Translator()

    # Act
    rst = translator.translate_tag(code)

    # Assert
    assert rst == "``Hello, World!``"


def test_rst_syntax_translator_translates_tag_codeblock():
    # Arrange
    text = TextNode("Hello, World!")
    codeblock = TagNode("codeblock", [text])

    translator = Translator()

    # Act
    rst = translator.translate_tag(codeblock)

    # Assert
    assert rst == dedent("""
    .. codeblock::  

       Hello, World!
    """).strip()


def test_rst_syntax_translator_translates_tag_codeblock_with_language():
    # Arrange
    text = TextNode("Hello, World!")
    codeblock = TagNode("codeblock", [text], {"language": "python"})

    translator = Translator()

    # Act
    rst = translator.translate_tag(codeblock)

    # Assert
    assert rst == dedent("""
    .. codeblock:: python 

       Hello, World!
    """).strip()


def test_rst_syntax_translator_translates_tag_link():
    # Arrange
    text = TextNode("Godocs")
    link = TagNode("link", [text], {
                   "url": "https://github.com/godocs-godot/godocs"})

    translator = Translator()

    # Act
    rst = translator.translate_tag(link)

    # Assert
    assert rst == "Godocs <https://github.com/godocs-godot/godocs>_"


def test_rst_syntax_translator_translates_reference():
    # Arrange
    text = TextNode("Godocs")
    link = TagNode("reference", [text], {"name": "RSTSyntaxTranslator"})

    translator = Translator()

    # Act
    rst = translator.translate_tag(link)

    # Assert
    assert rst == ":ref:`RSTSyntaxTranslator <RSTSyntaxTranslator>`"
