from argparse import ArgumentParser
from os import PathLike
from typing import Any, Optional, Sequence
from godocs.cli.command.cli_command import CLICommand
from godocs.cli.command.contruct import ConstructCommand
from godocs.util import module


class AppCommand(CLICommand):

    parser: ArgumentParser

    subparsers: Any

    construct: ConstructCommand

    def register_plugin(self, path: str | PathLike[str]):
        plugin = module.load("plugin", path)
        register = dict(module.get_functions(plugin))["register"]

        register(self.parser)

    def register(self, subparsers: Any):
        self.parser = ArgumentParser(description="Godot Docs generator CLI")

        self.parser.add_argument(
            "-p", "--plugin",
            help="Optional plugin script path to extend CLI."
        )
        self.parser.set_defaults(func=None)

        self.subparsers = self.parser.add_subparsers(
            title="command", description="The command to execute.")

        self.construct = ConstructCommand()

        self.construct.register(self.subparsers)

    def main(self, argv: Optional[Sequence[str]] = None):
        self.register(None)

        args, rest = self.parser.parse_known_args(argv)

        if args.plugin:
            self.register_plugin(args.plugin)

        args, rest = self.parser.parse_known_args(argv)

        self.parser.print_help()
        print(args)
        print(rest)

        if args.func is not None:
            args.func(args)
