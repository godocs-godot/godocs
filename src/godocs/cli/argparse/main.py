from argparse import ArgumentParser
from typing import Optional, Sequence
from os import PathLike
from godocs.cli.argparse.contruct import register
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
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers(
        title="command", description="The command to execute.")

    register(subparsers)

    args, rest = parser.parse_known_args(argv)

    if args.plugin:
        register_plugin(parser, args.plugin)

    args, rest = parser.parse_known_args(argv)

    parser.print_help()
    print(args)
    print(rest)

    if args.func is not None:
        args.func(args)


if __name__ == "__main__":
    main()
