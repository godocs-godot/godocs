from argparse import ArgumentParser
from typing import Any, TypedDict
from godocs.cli.command.cli_command import CLICommand
from godocs.cli.command.jinja_command import JinjaCommand


class ConstructCommands(TypedDict):
    jinja: JinjaCommand


class ConstructCommand(CLICommand):
    """
    A `CLICommand` that allows choosing a `constructor` for
    generating documentation.
    """

    TRANSLATORS = ["rst"]
    """
    The default translators accepted by this command.
    """

    parser: ArgumentParser
    """
    The `argparse.ArgumentParser` instance this `ConstructCommand` uses.
    """

    subparsers: Any | None = None
    """
    The `subparsers` of the `parser` of this `ConstructCommand`.
    """

    commands: ConstructCommands = {
        "jinja": JinjaCommand()
    }
    """
    The subcommands this `ConstructCommand` exposes.

    Currently, there's only the `"jinja"` option.
    """

    def register(self, subparsers: Any):
        """
        Registers this `ConstructCommand` as a subparser for the
        `subparsers` received.
        """

        self.parser = subparsers.add_parser(
            "construct", help="Construct documentation with a chosen backend")

        self.parser.add_argument(
            "-t", "--translator",
            default="rst",
            help=f"Which translator to use. Can be one of {self.TRANSLATORS} or a path to a script."
        )

        self.subparsers = self.parser.add_subparsers(
            title="constructor", description="The constructor to use.")

        self.commands["jinja"].register(self.subparsers)
