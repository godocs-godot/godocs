from godocs.cli.command.cli_command import CLICommand
from argparse import ArgumentParser, Namespace
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import _SubParsersAction  # type: ignore


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

    subparsers: "_SubParsersAction[ArgumentParser]"
    """
    The `subparsers` of the `parser` of this `ConstructCommand`.
    """

    parent_parser: ArgumentParser = ArgumentParser(add_help=False)
    """
    An `ArgumentParser` that holds common parameters and options for all
    the constructor types chosen.
    """

    subcommands: dict[str, CLICommand] = {}
    """
    The subcommands this `ConstructCommand` exposes.
    """

    def register(self, superparsers: "Optional[_SubParsersAction[ArgumentParser]]" = None):
        """
        Registers this `ConstructCommand` as a subparser for the
        `subparsers` received.
        """

        if superparsers is None:
            raise ValueError(
                'superparsers are needed for "construct" resistration')

        self.parser = superparsers.add_parser(
            "construct", help="Construct documentation with a chosen backend")

        self.parent_parser.add_argument(
            "-t", "--translator",
            default="rst",
            help=f"Which translator to use. Can be one of {self.TRANSLATORS} or a path to a script."
        )
        self.parent_parser.add_argument(
            "input_dir", help="Input directory with XML documentation files."
        )
        self.parent_parser.add_argument(
            "output_dir", help="Output directory to save generated documentation."
        )

        self.parser.set_defaults(execute=self.execute)

        self.subparsers = self.parser.add_subparsers(
            title="constructor", dest="constructor", description="The constructor to use.")

        # self.commands["jinja"].register(
        #     self.subparsers, self.subparsers_parent)

    def execute(self, args: Namespace):
        self.parser.print_help()
