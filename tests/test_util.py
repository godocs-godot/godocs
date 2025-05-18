import unittest
from pathlib import Path
import sys

from godocs.util import *

class TestUtil(unittest.TestCase):

  def test_load_module_returns_result(self):
    godocs = load_module("godocs", Path().joinpath("godocs").joinpath("__init__.py"))

    self.assertIsNotNone(godocs, "Godocs wasn't imported")

  def test_load_module_saves_in_modules(self):
    load_module("godocs", Path().joinpath("godocs").joinpath("__init__.py"))

    self.assertIsNotNone(sys.modules["godocs"], "Godocs wasn't imported")

  def test_get_functions_from_module_includes_a_function(self):
    function_names = list(map(
      lambda function_data: function_data[0],
      get_functions_from_module(util)
    ))

    self.assertIn("get_functions_from_module", function_names, "Function not got.")

  def test_find_returns_item(self):
    array = [ 1, 2, 3, 4 ]

    self.assertEqual(1, find(array, lambda item, i: item == 1), "Item not found")

  def test_find_returns_None(self):
    array = [ 1, 2, 3, 4 ]

    self.assertIsNone(find(array, lambda item, i: item == 5), "Item found")

if __name__ == "__main__":
  unittest.main()
