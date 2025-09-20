from os import PathLike
from pathlib import Path
from types import FunctionType
from typing import Callable, Any, cast
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from typing import TYPE_CHECKING

from godocs.util import dir, module
from godocs.constructor import Constructor
from godocs.constructor.constructor import ConstructorContext

type Builder = Callable[[
    Template, ConstructorContext, str | PathLike[str]], None]

MODELS_PATH = Path(__file__).parent / "models"
"""
The path to the directory containing the built-in **models** available for the `JinjaConstructor`.
This is set to `godocs/constructor/jinja_constructor/models`.
"""

DEFAULT_MODEL = "rst"
"""
The name of the default model from the built-in **models** used by the
`JinjaConstructor`, which defaults to `rst`.
"""

OUTPUT_TYPE = "rst"
"""
The type extension used by the files constructed with the `JinjaConstructor`.
"""


class JinjaConstructor(Constructor):
    """
    A specialized `Constructor` that uses the **Jinja** template language to
    build output documentation.

    Some important concepts for this class are:

    - Model: a model here refers to a **directory** where
             **Jinja** **templates** and **filters** are located.

    - Template: either a **folder** with an `index` file or a
                **Jinja** **file** with a **Jinja** template.

    - Filter: a function usable as a **Jinja** filter.

    - Builder: a function that receives a **Jinja** `Template`, a
               `ConstructorContext` and a folder `path`, and realizes the
               **creation** of one or more **output files inside** that `path`.

    For visualization, below is the structure of a model folder:

        <model>/
        ├── templates/
        │   ├── <template1.jinja>
        │   └── <template2>
        │       ├── <index.jinja>
        │       ├── <header.jinja>
        │       └── <footer.jinja>
        └── filters.py
    """

    models: list[Path] = []
    """
    A `list` with the default **models recognized** by this constructor,
    **got based** on the `MODELS_PATH` path.
    """

    model: Path | None = None
    """
    The **model** to be used by this constructor.
    """

    templates_path: Path | None = None
    """
    A **path** for a **directory** with the **templates**
    to be used with this constructor.
    """

    templates: list[Path] = []
    """
    A `list` with **templates** of this constructor,
    got **from** the `templates_path`.
    """

    filters: list[tuple[str, FunctionType]] = []
    """
    A `list` with `tuples` storing a **pair of name - filters**.
    These **filters** are got **from** the **model** chosen for
    this class, or from the `filters_path` passed to the **constructor**.
    """

    builders: dict[str, Builder] = {}
    """
    A `dict` with the **builders** this **constructor** should use.
    The **keys** here are the **names** of the `Builders`, and the
    **values** are the **builders themselves**.

    The **names** are important since they are what **link** what
    `templates` are gonna be passed to what **builders**.
    """

    def __init__(
        self,
        model: str | PathLike[str] | None = None,
        templates_path: str | PathLike[str] | None = None,
        filters_path: str | PathLike[str] | None = None,
        builders: dict[str, Builder] | None = None,
    ):
        """
        Instantiates a new `JinjaConstructor` with several optional customizations
        through parameters.

        Parameters:
            model: the **name** of the built-in **model** this constructor
                   should use or a **path** to a custom **model**.
                   By default, the `rst` model is chosen.
            templates_path: a **path** to a folder with **templates**
                            for use by this constructor.
                            Has precedence over the **templates path** got from
                            the chosen **model**.
                            By default, the `templates_path` is derived from the
                            `model` chosen.
            filters_path: a **path** to a **Python script** with **functions**
                          that can be used as **Jinja** filters by this constructor.
                          Has precedence over the **filters path** got from
                          the chosen **model**.
                          By default, the `filters_path` is derived from the
                          `model` chosen.
            builders: a `dict` mapping `str` names to `Builder` functions.
                      The name of the **templates** (file or folder name) is compared
                      with this `dict` to decide what `Builder` is used by what template.
                      By default, the `builders` support a `class` template -
                      which builds one output file for each class in the docs -
                      and an `index` template - which renders one file with an index for
                      all others.
        """

        self.models = self.find_models(MODELS_PATH)

        # model is either rst by default, or a built-in model
        # by name or a custom model by path
        if model is None:
            model = DEFAULT_MODEL
        if isinstance(model, str):
            self.model = self.find_model(model)
        if self.model is None:
            self.model = Path(model)

        # templates_path is either got from the model by default or
        # is got from the argument
        if templates_path is None:
            templates_path = self.model / "templates"

        self.templates_path = Path(templates_path)

        self.templates = self.find_templates(self.templates_path)

        # filters_path is either got from the model by default or
        # is got from the argument
        if filters_path is None:
            filters_path = self.model / "filters.py"

        self.filters = self.load_filters(Path(filters_path))

        if builders is None:
            builders = {
                "class": JinjaConstructor.construct_class_templates,
                "index": JinjaConstructor.construct_index_template,
            }

        self.builders = builders

    def find_models(self, path: Path) -> list[Path]:
        """
        Returns the paths of the built-in models available for this `JinjaConstructor`.

        This method searches in the file system for the modules in the `models` folder
        inside the `jinja_constructor` module (except for the __pycache__ folder).

        Returns:
          list[pathlib.Path]: List of Paths of the models.
        """

        models = dir.get_subdirs(
            path,
            exclude=["__pycache__"],
        )

        return models

    def find_model(self, name: str) -> Path | None:
        for model in self.models:
            if model.stem == name:
                return model

        return None

    def find_templates(self, path: Path) -> list[Path]:
        """
        Returns the paths of the templates of the given `model`.

        This method searches in the file system for the `templates` of the `model` provided,
        considering all folders or files in the `templates` directory to be templates
        (except for the __pycache__ folder).

        Returns:
          list[pathlib.Path]: List of Paths pointing of the templates.
        """

        templates = dir.get_subitems(
            path,
            exclude=["__pycache__"]
        )

        return templates

    def load_filters(self, path: Path) -> list[tuple[str, FunctionType]]:
        mod = module.load("filters", path)

        return module.get_functions(mod)

    def register_filters(self, env: Environment, filters: list[tuple[str, Callable[..., Any]]]) -> Environment:
        for filter in filters:
            env.filters[filter[0]] = filter[1]  # type: ignore

        return env

    @staticmethod
    def construct_template(
        name: str,
        template: Template,
        context: ConstructorContext,
        path: str | PathLike[str],
    ) -> None:
        path = Path(path)

        result = template.render(context)

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        with path.joinpath(f"{name}.{OUTPUT_TYPE}").open("w") as f:
            f.write(result)

    @staticmethod
    def construct_class_templates(
        template: Template,
        context: ConstructorContext,
        path: str | PathLike[str],
    ) -> None:
        for class_data in context["classes"]:
            context["current_class"] = class_data

            JinjaConstructor.construct_template(
                class_data["name"], template, context, path)

    @staticmethod
    def construct_index_template(
        template: Template,
        context: ConstructorContext,
        path: str | PathLike[str],
    ) -> None:
        JinjaConstructor.construct_template("index", template, context, path)

    def construct(self, context: ConstructorContext, path: str | PathLike[str]):
        env = Environment(
            loader=FileSystemLoader(self.templates_path),
            autoescape=select_autoescape()
        )

        self.register_filters(env, self.filters)

        for template_path in self.templates:
            builder = self.builders.get(template_path.stem)

            if builder is None:
                continue

            if template_path.is_dir():
                template_path = template_path / "index.jinja"

            # FIX: templates should be strings representing paths relative to the templates_path, not Paths
            template = env.get_template(template_path)

            builder(template, context, path)
