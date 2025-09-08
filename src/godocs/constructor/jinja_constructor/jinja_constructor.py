import importlib.util
import sys
import inspect
from os import PathLike
from pathlib import Path
from typing import Callable, Any
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from godocs.parser.context_creator import DocContext
    from godocs.constructor.constructor import TemplateMap

from godocs.constructor import Constructor


class JinjaConstructor(Constructor):

    # def __init__(self, model: str):
    #     self.model = model

    # def get_model_paths(self) -> list[Path]:
    #     """
    #     Returns the paths of the sub directories of this constructor's module.

    #     This method searches in the file system for the submodules of the jinja_constructor,
    #     considering all folders in it to be models (except for the __pycache__ folder).

    #     Returns:
    #       list[pathlib.Path]: List of Paths pointing to the model modules.
    #     """

    #     models = get_subdirs(
    #         Path(__file__).parent,
    #         exclude=["__pycache__"],
    #     )

    #     return models

    # def get_template_paths(self, model: Path) -> list[Path]:
    #     """
    #     Returns the paths of the templates of the given model.

    #     This method searches in the file system for the submodules of the templates of the model provided,
    #     considering all folders in it to be templates (except for the __pycache__ folder).

    #     Returns:
    #       list[pathlib.Path]: List of Paths pointing to the template folders.
    #     """

    #     templates = get_subdirs(
    #         model.joinpath("templates"),
    #         exclude=["__pycache__"]
    #     )

    #     return templates

    # def get_filters_path(self, model: Path) -> Path:
    #     return model.joinpath("filters.py")

    # def register_filters(self, env: Environment, filters: list[tuple[str, Callable[..., Any]]]) -> Environment:
    #     for filter in filters:
    #         env.filters[filter[0]] = filter[1]

    #     return env

    # def get_model_path(self, model_paths: list[Path]) -> Path:
    #     return next((path for path in model_paths if path.name == self.model), None)

    # def get_template_path(self, template_paths: list[Path], template: str) -> Path:
    #     return next((path for path in template_paths if path.name == template), None)

    def construct_class_references(
        self,
        template: Template,
        context: dict,
        build_path: str,
    ) -> None:
        context = context.copy()

        for class_data in context["classes"]:
            context["class"] = class_data

            result = template.render(context)

            build_path = Path(build_path).absolute()

            if not build_path.exists():
                build_path.mkdir(parents=True, exist_ok=True)

            with build_path.joinpath(context["class"]["name"].join("." + self.model)).open("w") as f:
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

    def construct(self, context: "DocContext", templates: "TemplateMap", path: str):

        filters_path = self.get_filters_path(model_path)

        filters_module = load_module("filters", filters_path)

        filters = get_functions_from_module(filters_module)

        env = Environment(
            loader=FileSystemLoader(class_reference_template_path),
            autoescape=select_autoescape()
        )

        for filter in filters:
            env.filters[filter[0]] = filter[1]

        template = env.get_template("index.jinja")

        self.construct_class_references(template, context, build_path)

        # print(template.render(context))
