from pathlib import Path

from godocs.constructor.jinja_constructor import JinjaConstructor
from godocs.constructor.jinja_constructor.jinja_constructor import Builder

TEST_FILTERS = """
def filter1(): return ""
def filter2(): return ""
def filter3(): return ""
"""

TEST_BUILDERS: dict[str, Builder] = {
    "builder1": lambda t, c, p: None,
    "builder2": lambda t, c, p: None,
    "builder3": lambda t, c, p: None,
}


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


def test_default_construction_with_model(tmp_path: Path):
    # Arrange
    model = tmp_path / "model"

    # Act
    constructor = JinjaConstructor(model=model)

    # Assert
    assert len(constructor.builders) == 2
    assert "class" in constructor.builders
    assert "index" in constructor.builders
    assert len(constructor.models) == 1
    assert constructor.models[0].stem == "rst"
    assert constructor.model is not None
    assert constructor.model.stem == "model"
    assert len(constructor.templates) == 0
    assert len(constructor.filters) == 0
    assert constructor.templates_path is not None
    assert constructor.templates_path.stem == "templates"
    assert constructor.templates_path.parent.stem == "model"


def test_default_construction_with_model_with_templates(tmp_path: Path):
    # Arrange
    model = tmp_path / "model"
    templates = model / "templates"

    templates.mkdir(parents=True, exist_ok=True)

    template1 = templates / "template1.jinja"
    template2 = templates / "template2"

    template1.touch()
    template2.mkdir()

    # Act
    constructor = JinjaConstructor(model=model)

    # Assert
    assert len(constructor.models) == 1
    assert constructor.models[0].stem == "rst"
    assert constructor.model is not None
    assert constructor.model.stem == "model"
    assert constructor.templates_path is not None
    assert constructor.templates_path.stem == "templates"
    assert constructor.templates_path.parent.stem == "model"
    assert len(constructor.templates) == 2
    assert constructor.templates[0].stem == "template1"
    assert constructor.templates[1].stem == "template2"
    assert len(constructor.filters) == 0
    assert len(constructor.builders) == 2
    assert "class" in constructor.builders
    assert "index" in constructor.builders


def test_default_construction_with_model_with_filters(tmp_path: Path):
    # Arrange
    model = tmp_path / "model"
    filters_script = model / "filters.py"

    model.mkdir()
    filters_script.write_text(TEST_FILTERS)

    # Act
    constructor = JinjaConstructor(model=model)

    # Assert
    assert len(constructor.models) == 1
    assert constructor.models[0].stem == "rst"
    assert constructor.model is not None
    assert constructor.model.stem == "model"
    assert constructor.templates_path is not None
    assert constructor.templates_path.stem == "templates"
    assert constructor.templates_path.parent.stem == "model"
    assert len(constructor.templates) == 0
    assert len(constructor.filters) == 3
    assert constructor.filters[0][0] == "filter1"
    assert constructor.filters[1][0] == "filter2"
    assert constructor.filters[2][0] == "filter3"
    assert len(constructor.builders) == 2
    assert "class" in constructor.builders
    assert "index" in constructor.builders


def test_default_construction_with_templates_path(tmp_path: Path):
    # Arrange
    templates_path = tmp_path / "custom_templates"
    template1 = templates_path / "template1.jinja"
    template2 = templates_path / "template2"

    templates_path.mkdir(parents=True, exist_ok=True)
    template1.touch()
    template2.mkdir()

    # Act
    constructor = JinjaConstructor(templates_path=templates_path)

    # Assert
    assert len(constructor.models) == 1
    assert constructor.models[0].stem == "rst"
    assert constructor.model is not None
    assert constructor.model.stem == "rst"
    assert constructor.templates_path is not None
    assert constructor.templates_path.stem == "custom_templates"
    assert len(constructor.templates) == 2
    assert constructor.templates[0].stem == "template1"
    assert constructor.templates[1].stem == "template2"
    assert len(constructor.filters) == 7
    assert len(constructor.builders) == 2
    assert "class" in constructor.builders
    assert "index" in constructor.builders


def test_default_construction_with_filters_path(tmp_path: Path):
    # Arrange
    filters_path = tmp_path / "custom_filters.py"

    filters_path.write_text(TEST_FILTERS)

    # Act
    constructor = JinjaConstructor(filters_path=filters_path)

    # Assert
    assert len(constructor.models) == 1
    assert constructor.models[0].stem == "rst"
    assert constructor.model is not None
    assert constructor.model.stem == "rst"
    assert constructor.templates_path is not None
    assert constructor.templates_path.stem == "templates"
    assert len(constructor.templates) == 2
    assert constructor.templates[0].stem == "class"
    assert constructor.templates[1].stem == "index"
    assert len(constructor.filters) == 3
    assert constructor.filters[0][0] == "filter1"
    assert constructor.filters[1][0] == "filter2"
    assert constructor.filters[2][0] == "filter3"
    assert len(constructor.builders) == 2
    assert "class" in constructor.builders
    assert "index" in constructor.builders


def test_default_construction_with_builders():
    # Act
    constructor = JinjaConstructor(builders=TEST_BUILDERS)

    # Assert
    assert len(constructor.models) == 1
    assert constructor.models[0].stem == "rst"
    assert constructor.model is not None
    assert constructor.model.stem == "rst"
    assert constructor.templates_path is not None
    assert constructor.templates_path.stem == "templates"
    assert len(constructor.templates) == 2
    assert constructor.templates[0].stem == "class"
    assert constructor.templates[1].stem == "index"
    assert len(constructor.filters) == 7
    assert len(constructor.builders) == 3
    assert "builder1" in constructor.builders
    assert "builder2" in constructor.builders
    assert "builder3" in constructor.builders
