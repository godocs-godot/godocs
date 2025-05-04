from pathlib import Path
from jinja2 import (
  Environment,
  PackageLoader,
  FileSystemLoader,
  select_autoescape,
)
from util import load_module, get_functions_from_module, get_subdirs

def get_constructor_paths() -> list[Path]:
  constructors_path = Path(__file__).parent

  constructors = get_subdirs(constructors_path, exclude=[ "__pycache__" ])

  return constructors

def get_template_paths(constructor: Path) -> list[Path]:
  templates_path = constructor.joinpath("templates")

  templates = get_subdirs(templates_path, exclude=[ "__pycache__" ])

  return templates

def get_filters_path(constructor: Path) -> Path:
  return constructor.joinpath("filters.py")

def register_filters(env: Environment, filters: list[tuple]) -> Environment:
  for filter in filters:
    env.filters[filter[0]] = filter[1]
  
  return env

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

def construct(constructor):
  print()

  constructor_paths = get_constructor_paths()

  rst_constructor_path = constructor_paths[0]

  template_paths = get_template_paths(rst_constructor_path)

  class_reference_template_path = template_paths[1]

  filters_path = get_filters_path(rst_constructor_path)

  filters_module = load_module("filters", filters_path)

  filters = get_functions_from_module(filters_module)
  
  env = Environment(
      loader=FileSystemLoader(class_reference_template_path),
      autoescape=select_autoescape()
  )
  
  register_filters(env, filters)

  template = env.get_template("index.jinja")

  print(template.render(context))
