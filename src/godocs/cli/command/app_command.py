from argparse import ArgumentParser, Namespace
from os import PathLike
from typing import Any, Optional, Sequence, TypedDict, Callable
from godocs.cli.command.cli_command import CLICommand
from godocs.cli.command.contruct_command import ConstructCommand
from godocs.util import module


class AppCommands(TypedDict):
    construct: ConstructCommand


type RegisterPlugin = Callable[[AppCommand], None]


class AppCommand(CLICommand):
    """
    The main `CLICommand` for the `godocs` app.

    This command exposes as its main (and only, for now) option the
    `"construct"` subcommand, which triggers the generation of
    documentation output.

    It's possible to extend the functionality of this CLI app
    by providing a path to a script in the `--plugin` or `-p`
    option.
    That script should have a function called `register` with
    its signature expecting an `AppCommand` as its parameter.

    That function can then make any modifications/ additions
    to the application parsers and subparsers as needed.
    """

    parser: ArgumentParser
    """
    The `argparse.ArgumentParser` instance this `AppCommand` uses.
    """

    subparsers: Any | None = None
    """
    The `subparsers` of the `parser` of this `AppCommand`.
    """

    commands: AppCommands = {
        "construct": ConstructCommand()
    }
    """
    The subcommands this `AppCommand` exposes.

    Currently, there's only the `"construct"` option.
    """

    def register_plugin(self, path: str | PathLike[str]):
        plugin = module.load("plugin", path)
        register: RegisterPlugin | None = dict(
            module.get_functions(plugin)).get("register")

        if register is None:
            raise NotImplementedError(
                f"Plugin {path} needs to implement a register function")

        register(self)

    def exec(self, args: Namespace):
        self.parser.print_help()

    def register(self, subparsers: Any | None = None):
        """
        Creates the `parser` for this `AppCommand` and
        registers its options, parameters and subcommands.
        """

        self.parser = ArgumentParser(description="Godot Docs generator CLI")

        self.parser.add_argument(
            "-p", "--plugin",
            help="Optional plugin script path to extend CLI."
        )
        self.parser.set_defaults(func=self.exec)

        self.subparsers = self.parser.add_subparsers(
            title="command", description="The command to execute.")

        self.commands["construct"].register(self.subparsers)

    def main(self, argv: Optional[Sequence[str]] = None):
        self.register()

        args, rest = self.parser.parse_known_args(argv)

        if args.plugin:
            self.register_plugin(args.plugin)

        args, rest = self.parser.parse_known_args(argv)

        print(args)
        print(rest)

        if args.func is not None:
            args.func(args)
