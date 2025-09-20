from godocs.constructor.jinja_constructor import JinjaConstructor


def test_default_construction():
    # Act
    constructor = JinjaConstructor()

    # Assert
    assert len(constructor.builders) == 2
    assert "class" in constructor.builders
    assert "index" in constructor.builders
    assert len(constructor.filters) == 7
    assert constructor.model is not None
    assert constructor.model.stem == "rst"
    assert len(constructor.models) == 1
    assert constructor.models[0].stem == "rst"
    assert len(constructor.templates) == 2
    assert constructor.templates[0].stem == "class"
    assert constructor.templates[1].stem == "index"
    assert constructor.templates_path is not None
    assert constructor.templates_path.stem == "templates"
    assert constructor.templates_path.parent.stem == "rst"
