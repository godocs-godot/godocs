from argparse import ArgumentParser
from typing import Any
from godocs.cli import jinja

TRANSLATORS = ["rst"]


def register(subparsers: Any):
    construct_parser: ArgumentParser = subparsers.add_parser(
        "construct", help="Construct documentation with a chosen backend")

    construct_parser.add_argument(
        "-t", "--translator",
        default="rst",
        help=f"Which translator to use. Can be one of {TRANSLATORS} or a path to a script."
    )

    construct_subparsers = construct_parser.add_subparsers(
        title="constructor", description="The constructor to use.")

    jinja.register(construct_subparsers)
