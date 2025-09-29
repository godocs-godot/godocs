from argparse import ArgumentParser, Namespace
from typing import Any
from godocs.cli.command.cli_command import CLICommand


class JinjaCommand(CLICommand):
    """
    A `CLICommand` that allows defining the behavior of the
    `jinja_constructor`.
    """

    MODELS = ["rst"]
    """
    The default models accepted by this command.
    """

    parser: ArgumentParser
    """
    The `argparse.ArgumentParser` instance this `JinjaCommand` uses.
    """

    def exec(self, args: Namespace):
        """
        Executes the main logic of this command with the parsed `args`.
        """
        self.parser.print_help()

        print("\n[Godocs Construct Jinja]")
        print(args)

    def register(self, subparsers: Any | None = None, parent: ArgumentParser | None = None):
        """
        Registers this `JinjaCommand` as a subparser for the
        `subparsers` received.
        """

        if subparsers is None:
            raise ValueError('subparsers is needed for "jinja" resistration')

        self.parser: ArgumentParser = subparsers.add_parser(
            "jinja", help="Construct docs using the Jinja constructor.", parents=[parent])

        self.parser.add_argument(
            "-m", "--model",
            default="rst",
            help=f"Which model to use. Can be one of {JinjaCommand.MODELS} or a path to a model directory."
        )
        self.parser.add_argument(
            "-T", "--templates",
            help="Path to directory with Jinja templates."
        )
        self.parser.add_argument(
            "-F", "--filters",
            help="Path to script with Jinja filter functions."
        )
        self.parser.add_argument(
            "-B", "--builders",
            help="Path to script with builders dict."
        )
        self.parser.set_defaults(func=self.exec)
