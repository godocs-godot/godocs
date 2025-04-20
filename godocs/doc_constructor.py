from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape
from filters import *

env = Environment(
    loader=FileSystemLoader("godocs/templates/rst/"),
    autoescape=select_autoescape()
)

env.filters["make_code_member_label_target"] = make_code_member_label_target
env.filters["join_code_member_name"] = join_code_member_name
env.filters["make_code_member_ref"] = make_code_member_ref
env.filters["make_code_member_type_ref"] = make_code_member_type_ref
env.filters["make_property_signature"] = make_property_signature
env.filters["make_method_signature"] = make_method_signature

template = env.get_template("class_reference.rst")

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
  },
}

print(template.render(context))
