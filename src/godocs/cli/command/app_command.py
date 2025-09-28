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
        registers the `--plugin` or `-p` option, as well
        as sets the help printing function as the default
        behavior when nothing else is chosen.
        """

        self.parser = ArgumentParser(description="Godot Docs generator CLI")

        self.parser.add_argument(
            "-p", "--plugin",
            help="Optional plugin script path to extend CLI."
        )
        self.parser.set_defaults(func=self.exec)

    def register_subparsers(self):
        """
        Registers the subparsers for this `AppCommand`.

        This method was separated from the `register` because
        this way parsing can be realized before and after
        the native subcommands are registered, avoiding errors
        with unknown subparsers that are registered after in
        plugin code.
        """

        self.subparsers = self.parser.add_subparsers(
            title="command", description="The command to execute.")

        self.commands["construct"].register(self.subparsers)

    def main(self, argv: Optional[Sequence[str]] = None):
        """
        Entrypoint for the `AppCommand` to be parsed and executed,
        as well as to register plugins in the way.
        """

        # Creates the main parser.
        self.register()

        # Parses args looking solely for the --plugin option.
        args, _ = self.parser.parse_known_args(argv)

        # Registers main parser's subparsers.
        self.register_subparsers()

        # If a plugin script was provided, execute it.
        if args.plugin:
            self.register_plugin(args.plugin)

        # Parse again, this time with plugin features.
        args, _ = self.parser.parse_known_args(argv)

        # Execute main args.func.
        if args.func is not None:
            args.func(args)
