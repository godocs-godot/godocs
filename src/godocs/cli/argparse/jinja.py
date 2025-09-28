from argparse import ArgumentParser, Namespace
from typing import Any

MODELS = ["rst"]


def jinja(args: Namespace):
    print(f"[Jinja] Model: {args.model}")
    print(f"[Jinja] Templates: {args.templates}")
    print(f"[Jinja] Filters: {args.filters}")
    print(f"[Jinja] Builders: {args.builders}")
    print(f"[Jinja] In: {args.input_dir}, Out: {args.output_dir}")


def register(subparsers: Any):
    jinja_parser: ArgumentParser = subparsers.add_parser(
        "jinja", help="Construct docs using the Jinja constructor.")

    jinja_parser.add_argument(
        "-m", "--model",
        default="rst",
        help=f"Which model to use. Can be one of {MODELS} or a path to a model directory."
    )
    jinja_parser.add_argument(
        "-T", "--templates",
        help="Path to directory with Jinja templates."
    )
    jinja_parser.add_argument(
        "-F", "--filters",
        help="Path to script with Jinja filter functions."
    )
    jinja_parser.add_argument(
        "-B", "--builders",
        help="Path to script with builders dict."
    )
    jinja_parser.add_argument(
        "input_dir", help="Input directory with XML documentation files."
    )
    jinja_parser.add_argument(
        "output_dir", help="Output directory to save generated documentation."
    )
    jinja_parser.set_defaults(func=jinja)
