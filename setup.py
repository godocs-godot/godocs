from setuptools import setup, find_packages

with open("README.md", 'r') as f:
  description = f.read()

setup(
  name="godocs",
  version="0.1",
  author="Daniel Sousa (nadjiel)",
  author_email="<oliveira.daaaaniel@gmail.com>",
  description="Godocs is a package that helps in the process of building Godot documentation.",
  keywords=[ "python", "godot", "documentation", "docs", "godocs", "sphinx", "jinja2" ],
  packages=find_packages(),
  install_requires=[],
  entry_points={
    "console_scripts": [
      "godocs = godocs:parse",
    ],
  },
  long_description=description,
  long_description_content_type="text/markdown",
  classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.13",
    "Operating System :: OS Independent",
  ],
)
