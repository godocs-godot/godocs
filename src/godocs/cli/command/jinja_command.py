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

        print(f"[Jinja] Model: {args.model}")
        print(f"[Jinja] Templates: {args.templates}")
        print(f"[Jinja] Filters: {args.filters}")
        print(f"[Jinja] Builders: {args.builders}")
        print(f"[Jinja] In: {args.input_dir}, Out: {args.output_dir}")

    def register(self, subparsers: Any):
        """
        Registers this `JinjaCommand` as a subparser for the
        `subparsers` received.
        """

        self.parser: ArgumentParser = subparsers.add_parser(
            "jinja", help="Construct docs using the Jinja constructor.")

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
        self.parser.add_argument(
            "input_dir", help="Input directory with XML documentation files."
        )
        self.parser.add_argument(
            "output_dir", help="Output directory to save generated documentation."
        )
        self.parser.set_defaults(func=self.exec)
