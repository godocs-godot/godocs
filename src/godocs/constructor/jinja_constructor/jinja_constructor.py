import importlib.util
import sys
import inspect
from os import PathLike
from pathlib import Path
from types import FunctionType
from typing import Callable, Any
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from typing import TYPE_CHECKING

from godocs.util import dir, module

if TYPE_CHECKING:
    from godocs.parser.context_creator import DocContext

from godocs.constructor import Constructor


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

    def __init__(
        self,
        model: str | None = None,
        templates: list[Path] | None = None,
        filters: list[tuple[str, FunctionType]] | None = None
    ):
        self.models = self.find_models()

        if model is None:
            model = "rst"

        self.model = self.find_model(model)

        if templates is None:
            templates = self.find_templates(self.model)
        if filters is None:
            filters = self.load_filters(self.model)

        self.templates = templates
        self.filters = self.load_filters(self.model)

    def find_models(self) -> list[Path]:
        """
        Returns the paths of the built-in models available for this `JinjaConstructor`.

        This method searches in the file system for the modules in the `models` folder
        inside the `jinja_constructor` module (except for the __pycache__ folder).

        Returns:
          list[pathlib.Path]: List of Paths of the models.
        """

        models = dir.get_subdirs(
            Path(__file__).parent / "models",
            exclude=["__pycache__"],
        )

        return models

    def find_model(self, name: str) -> Path:
        for model in self.models:
            if model.stem == name:
                return model

        raise ModuleNotFoundError(
            f"Model {name} not found. The models available are {self.models}.")

    def find_templates(self, model: Path) -> list[Path]:
        """
        Returns the paths of the templates of the given `model`.

        This method searches in the file system for the `templates` of the `model` provided,
        considering all folders or files in the `templates` directory to be templates
        (except for the __pycache__ folder).

        Returns:
          list[pathlib.Path]: List of Paths pointing of the templates.
        """

        [template for template in (model / "templates").iterdir()]

        templates = dir.get_subitems(
            model / "templates",
            exclude=["__pycache__"]
        )

        return templates

    def find_filters(self, model: Path) -> Path:
        return model / "filters.py"

    def load_filters(self, model: Path) -> list[tuple[str, FunctionType]]:
        mod = module.load("filters", model / "filters.py")

        return module.get_functions(mod)

    def register_filters(self, env: Environment, filters: list[tuple[str, Callable[..., Any]]]) -> Environment:
        for filter in filters:
            env.filters[filter[0]] = filter[1]

        return env

    # def get_model_path(self, model_paths: list[Path]) -> Path:
    #     return next((path for path in model_paths if path.name == self.model), None)

    # def get_template_path(self, template_paths: list[Path], template: str) -> Path:
    #     return next((path for path in template_paths if path.name == template), None)

    def construct_class_references(
        self,
        template: Template,
        context: "DocContext",
        path: str,
    ) -> None:
        context = context.copy()

        for class_data in context["classes"]:
            context["class"] = class_data

            result = template.render(context)

            path = Path(path).absolute()

            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)

            with path.joinpath(context["class"]["name"].join("." + self.model)).open("w") as f:
                f.write(result)

    # def construct(self, context: "DocContext", build_path: str):
    #     model_paths = self.get_model_paths()

    #     model_path = self.get_model_path(model_paths)

    #     template_paths = self.get_template_paths(model_path)

    #     class_index_template_path = self.get_template_path(
    #         template_paths, "class_index")
    #     class_reference_template_path = self.get_template_path(
    #         template_paths, "class_reference")

    #     filters_path = self.get_filters_path(model_path)

    #     filters_module = load_module("filters", filters_path)

    #     filters = get_functions_from_module(filters_module)

    #     env = Environment(
    #         loader=FileSystemLoader(class_reference_template_path),
    #         autoescape=select_autoescape()
    #     )

    #     self.register_filters(env, filters)

    #     template = env.get_template("index.jinja")

    #     self.construct_class_references(template, context, build_path)

    #     # print(template.render(context))
