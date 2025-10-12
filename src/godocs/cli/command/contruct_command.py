from argparse import ArgumentParser, Namespace
from typing import Any
from godocs.cli.command.cli_command import CLICommand

# TODO: add integration with jinja commands (through the plugin, though this warning is here)


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

    subparsers_parent: ArgumentParser = ArgumentParser(add_help=False)
    """
    An `ArgumentParser` that holds common parameters and options for all
    the constructor types chosen.
    """

    commands: dict[str, CLICommand] = {}
    """
    The subcommands this `ConstructCommand` exposes.
    """

    def exec(self, args: Namespace):
        self.parser.print_help()

        print("\n[Godocs Construct]")
        print(args)

    def register(self, subparsers: Any | None = None, parent: ArgumentParser | None = None):
        """
        Registers this `ConstructCommand` as a subparser for the
        `subparsers` received.
        """

        if subparsers is None:
            raise ValueError(
                'subparsers is needed for "construct" resistration')

        self.parser = subparsers.add_parser(
            "construct", help="Construct documentation with a chosen backend")

        self.subparsers_parent.add_argument(
            "-t", "--translator",
            default="rst",
            help=f"Which translator to use. Can be one of {self.TRANSLATORS} or a path to a script."
        )
        self.subparsers_parent.add_argument(
            "input_dir", help="Input directory with XML documentation files."
        )
        self.subparsers_parent.add_argument(
            "output_dir", help="Output directory to save generated documentation."
        )

        self.parser.set_defaults(func=self.exec)

        self.subparsers = self.parser.add_subparsers(
            title="constructor", dest="constructor", description="The constructor to use.")

        self.commands["jinja"].register(
            self.subparsers, self.subparsers_parent)
