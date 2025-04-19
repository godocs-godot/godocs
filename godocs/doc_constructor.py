from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("godocs/templates/rst/"),
    autoescape=select_autoescape()
)

template = env.get_template("heading.rst")

context = {
  "ref_prefix": "godocs",
  "class": {
    "name": "Class",
    "parents": [ "SuperClass", "GrandClass", "ImenseClass" ],
    "brief_description": "This is a Class",
  },
}

print(template.render(context))
