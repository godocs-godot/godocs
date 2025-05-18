from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from godocs.util import load_module, get_functions_from_module, get_subdirs
from godocs.constructor import Constructor

class JinjaConstructor(Constructor):

  def __init__(self, type: str):
    self.type = type

  def get_model_paths(self) -> list[Path]:
    """
    Returns the paths of the sub directories of this constructor's module.

    This method searches in the file system for the submodules of the jinja_constructor,
    considering all folders in it to be models (except for the __pycache__ folder).

    Returns:
      list[pathlib.Path]: List of Paths pointing to the model modules.
    """

    models = get_subdirs(
      Path(__file__).parent,
      exclude=[ "__pycache__" ],
    )

    return models

  def get_template_paths(self, model: Path) -> list[Path]:
    """
    Returns the paths of the templates of the given model.

    This method searches in the file system for the submodules of the templates of the model provided,
    considering all folders in it to be templates (except for the __pycache__ folder).

    Returns:
      list[pathlib.Path]: List of Paths pointing to the template folders.
    """

    templates = get_subdirs(
      model.joinpath("templates"),
      exclude=[ "__pycache__" ]
    )

    return templates

  def get_filters_path(self, model: Path) -> Path:
    return model.joinpath("filters.py")

  def register_filters(self, env: Environment, filters: list[tuple]) -> Environment:
    for filter in filters:
      env.filters[filter[0]] = filter[1]
    
    return env

  def construct(self, context: dict):
    constructor_paths = self.get_model_paths()

    rst_constructor_path = constructor_paths[0]

    template_paths = self.get_template_paths(rst_constructor_path)

    class_reference_template_path = template_paths[1]

    filters_path = self.get_filters_path(rst_constructor_path)

    filters_module = load_module("filters", filters_path)

    filters = get_functions_from_module(filters_module)
    
    env = Environment(
        loader=FileSystemLoader(class_reference_template_path),
        autoescape=select_autoescape()
    )
    
    self.register_filters(env, filters)

    template = env.get_template("index.jinja")

    print(template.render(context))
