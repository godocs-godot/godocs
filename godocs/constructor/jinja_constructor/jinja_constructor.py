from pathlib import Path
from jinja2 import (
  Environment,
  FileSystemLoader,
  select_autoescape,
)

from util import load_module, get_functions_from_module, get_subdirs
from constructor import Constructor

context = {
  "ref_prefix": "godocs",
  "class": {
    "name": "Class",
    "parents": [ "SuperClass", "GrandClass", "ImenseClass.InnerClass" ],
    "brief_description": "This is a Class",
    "description": "This is a long description.",
    "properties": [
      {
        "name": "property_a",
        "type": "Array[String]",
        "default": '""',
        "description": "A very convenient property.",
      },
      {
        "name": "property_b",
        "type": "Dictionary[int, int]",
        "default": '{}',
        "description": "A very convenient Dictionary.",
      },
    ],
    "methods": [
      {
        "name": "method_a",
        "type": "Array[String]",
        "args": [
          {
            "name": "arg1",
            "type": "int",
            "default": "0",
          }
        ],
        "description": "A very convenient method.",
      },
      {
        "name": "method_b",
        "type": "Dictionary[int, bool]",
        "args": [
          {
            "name": "arg",
            "type": "RegEx",
            "default": "new()",
          }
        ],
        "description": "Another very convenient method.",
      },
    ],
    "signals": [
      {
        "name": "signal_a",
        "args": [
          {
            "name": "arg1",
            "type": "int",
            "default": "0",
          }
        ],
        "description": "A very convenient signal.",
      },
      {
        "name": "signal_b",
        "args": [
          {
            "name": "arg",
            "type": "RegEx",
            "default": "new()",
          }
        ],
        "description": "Another very convenient signal.",
      },
    ],
    "constants": [
      {
        "name": "CONSTANT_A",
        "type": "String",
        "value": '""',
        "description": "A very convenient constant.",
      },
      {
        "name": "CONSTANT_B",
        "type": "bool",
        "value": 'false',
        "description": "Another very convenient constant.",
      },
    ],
    "enums": [
      {
        "name": "EnumA",
        "values": [
          {
            "name": "EnumA.CONSTANT1",
            "value": '0',
            "description": "A very convenient constant.",
          },
          {
            "name": "EnumA.CONSTANT2",
            "value": '1',
            "description": "A very convenient constant.",
          },
        ],
        "description": "A very convenient Enum.",
      },
      {
        "name": "EnumB",
        "values": [
          {
            "name": "EnumB.CONSTANT1",
            "value": '0',
            "description": "A very convenient constant.",
          },
          {
            "name": "EnumB.CONSTANT2",
            "value": '1',
            "description": "A very convenient constant.",
          },
        ],
        "description": "A very convenient Enum.",
      },
    ],
  },
}

class JinjaConstructor(Constructor):

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

  def construct(self, constructor):
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
