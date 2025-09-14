from os import PathLike
from pathlib import Path
from types import FunctionType
from typing import Callable, Any, cast
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from typing import TYPE_CHECKING

from godocs.util import dir, module

if TYPE_CHECKING:
    from godocs.constructor.constructor import ConstructorContext

from godocs.constructor import Constructor

DEFAULT_MODEL = "rst"

CONSTRUCTED_TYPE = "rst"


class JinjaConstructor(Constructor):
    """
    A specialized `Constructor` that uses the `jinja` template language to
    build the output documentation.

    On initialization, this class can receive a couple arguments:
    - `model`: the **name** of the built-in **model** this constructor
               should use or a **path** to a custom **model**.
    - `templates`: a list with the paths of the `jinja` **templates** that
                   should be used to build the documentation.
    - `filters`: a list of tuples with `str`-`function` pairs representing
                 the filters that the jinja engine is going to need
                 when using the templates to build the docs.

    In this class, the concept of `models` is a folder (or module) that
    holds has the following structure:

        <model>/
        ├── templates/
        │   ├── <template1.jinja>
        │   └── <template2>/index.jinja>
        └── filters.py
    """

    models_path: Path = Path(__file__).parent / "models"

    models: list[Path] = []

    model: Path | None = None

    templates: list[Path] = []

    filters: list[tuple[str, FunctionType]] = []

    def __init__(
        self,
        models_path: str | PathLike[str] | None = None,
        model: str | PathLike[str] | None = None,
        templates_path: str | PathLike[str] | None = None,
        templates: list[Path] | None = None,
        filters_path: str | PathLike[str] | None = None,
        filters: list[tuple[str, FunctionType]] | None = None,
    ):
        if models_path is not None:
            self.models_path = Path(models_path)

        self.models = self.find_models(self.models_path)

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
        # templates is got from the default path or from the argument
        if templates is None:
            templates = self.find_templates(Path(templates_path))

        # filters_path is either got from the model by default or
        # is got from the argument
        if filters_path is None:
            filters_path = self.model / "filters.py"
        # filters is got from the default path or from the argument
        if filters is None:
            filters = self.load_filters(Path(filters_path))

        self.templates = templates
        self.filters = filters

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

    def construct_template(
        self,
        name: str,
        template: Template,
        context: ConstructorContext,
        path: str | PathLike[str],
    ) -> None:
        path = Path(path)

        result = template.render(context)

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        with path.joinpath(f"{name}.{CONSTRUCTED_TYPE}").open("w") as f:
            f.write(result)

    def construct_class_templates(
        self,
        template: Template,
        context: ConstructorContext,
        path: str | PathLike[str],
    ) -> None:
        for class_data in context["classes"]:
            context["current_class"] = class_data

            self.construct_template(
                class_data["name"], template, context, path)

    def construct_index_template(
        self,
        template: Template,
        context: ConstructorContext,
        path: str | PathLike[str],
    ) -> None:
        self.construct_template("index", template, context, path)

    def construct(self, context: ConstructorContext, path: str | PathLike[str]):
        print("not implemented")

        # env = Environment(
        #     loader=FileSystemLoader(class_reference_template_path),
        #     autoescape=select_autoescape()
        # )

        # self.register_filters(env, filters)

        # template = env.get_template("index.jinja")

        # self.construct_class_references(template, context, build_path)

        # print(template.render(context))
