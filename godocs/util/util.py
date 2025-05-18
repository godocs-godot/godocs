from os import PathLike
import importlib.util
import sys
import inspect
from pathlib import Path

def load_module(name: str, path: str | PathLike):
  spec = importlib.util.spec_from_file_location(name, path)
  module = importlib.util.module_from_spec(spec)

  # Register in sys.modules
  sys.modules[name] = module
  spec.loader.exec_module(module)

  return module

def get_functions_from_module(module: object):
  return list(filter(
    lambda function_data: function_data[1].__module__ == module.__name__,
    inspect.getmembers(module, inspect.isfunction)
  ))

def get_subdirs(
  path: str | PathLike,
  exclude: list[str] = None,
  include: list[str] = None,
) -> list[Path]:
  if exclude == None:
    exclude = []
  if include == None:
    include = []

  path = Path(path)
  
  subdirs = []

  for p in path.iterdir():
    if not p.is_dir():
      continue
    if p.name in exclude:
      continue
    if len(include) > 0 and not p.name in include:
      continue
    
    subdirs.append(p)

  return subdirs

def find(iter, callback):
  return next((item for i, item in enumerate(iter) if callback(item, i)), None)
