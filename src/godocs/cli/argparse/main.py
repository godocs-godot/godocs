# # main.py
# import argparse
# import sys
# from typing import Sequence, Optional
# from godocs.util.module import load, get_functions


# TRANSLATORS = ["rst"]
# MODELS = ["rst"]


# def construct_jinja(args: argparse.Namespace):
#     """
#     Construct docs using the Jinja constructor.
#     """
#     print(f"[Jinja] Model: {args.model}")
#     print(f"[Jinja] Templates: {args.templates}")
#     print(f"[Jinja] Filters: {args.filters}")
#     print(f"[Jinja] Builders: {args.builders}")
#     print(f"[Jinja] In: {args.input_dir}, Out: {args.output_dir}")


# def add_construct_parser(subparsers):
#     """
#     Adds the 'construct' subparser and its subcommands.
#     """
#     construct_parser = subparsers.add_parser(
#         "construct", help="Construct documentation with a chosen backend"
#     )
#     construct_parser.add_argument(
#         "-t", "--translator",
#         default="rst",
#         help=f"Which translator to use. Can be one of {TRANSLATORS} or a path to a script."
#     )

#     # Nested subcommands inside construct
#     construct_subparsers = construct_parser.add_subparsers(
#         dest="construct_command")

#     # ---- jinja ----
#     jinja_parser = construct_subparsers.add_parser(
#         "jinja", help="Construct docs using the Jinja constructor."
#     )
#     jinja_parser.add_argument(
#         "-m", "--model",
#         default="rst",
#         help=f"Which model to use. Can be one of {MODELS} or a path to a model directory."
#     )
#     jinja_parser.add_argument(
#         "-T", "--templates",
#         help="Path to directory with Jinja templates."
#     )
#     jinja_parser.add_argument(
#         "-F", "--filters",
#         help="Path to script with Jinja filter functions."
#     )
#     jinja_parser.add_argument(
#         "-B", "--builders",
#         help="Path to script with builders dict."
#     )
#     jinja_parser.add_argument(
#         "input_dir", help="Input directory with XML documentation files."
#     )
#     jinja_parser.add_argument(
#         "output_dir", help="Output directory to save generated documentation."
#     )
#     jinja_parser.set_defaults(func=construct_jinja)


# def main(argv: Optional[Sequence[str]] = None):
#     parser = argparse.ArgumentParser(
#         description="Godot Docs generator CLI"
#     )

#     parser.add_argument(
#         "-p", "--plugin",
#         help="Optional plugin script path to extend CLI."
#     )

#     subparsers = parser.add_subparsers(dest="command")

#     # construct
#     add_construct_parser(subparsers)

#     args = parser.parse_args(argv)

#     # Plugin handling
#     if args.plugin:
#         custom = load("plugin", args.plugin)
#         command = [f for f in get_functions(custom) if f[0] == "command"][0]
#         command[1](parser)  # Pass parser so plugin can register commands

#     # Execute command function
#     if hasattr(args, "func"):
#         args.func(args)
#     else:
#         parser.print_help()


# if __name__ == "__main__":
#     main()

from argparse import ArgumentParser
from typing import Optional, Sequence
from os import PathLike
from godocs.util import module


def register_plugin(parser: ArgumentParser, path: str | PathLike[str]):
    plugin = module.load("plugin", path)
    register = dict(module.get_functions(plugin))["register"]

    register(parser)


def main(argv: Optional[Sequence[str]] = None):
    parser = ArgumentParser(description="Godot Docs generator CLI")

    parser.add_argument(
        "-p", "--plugin",
        help="Optional plugin script path to extend CLI."
    )

    args, rest = parser.parse_known_args(argv)

    if args.plugin:
        register_plugin(parser, args.plugin)

    args, rest = parser.parse_known_args(argv)

    parser.print_help()
    print(args)
    print(rest)


if __name__ == "__main__":
    main()
