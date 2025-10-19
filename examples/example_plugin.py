from argparse import Namespace, ArgumentParser
from pprint import pprint
from typing import Optional, TYPE_CHECKING
from godocs.plugin import Plugin as BasePlugin
from godocs.cli import AppCommand, CLICommand
from godocs.cli.command.cli_command import Processor

if TYPE_CHECKING:
    from argparse import _SubParsersAction  # type: ignore


class ExampleCommand(CLICommand):

    def register(
        self,
        superparsers: "Optional[_SubParsersAction[ArgumentParser]]" = None,
        parent_parser: Optional[ArgumentParser] = None,
        processors: Optional[list[Processor]] = None
    ):
        if superparsers is None:
            raise ValueError(
                'superparsers is needed for "example" registration')
        if parent_parser is None:
            raise ValueError(
                'parent_parser is needed for "example" registration')

        self.parser: ArgumentParser = superparsers.add_parser(
            "example", help="Construct docs using an Example constructor.", parents=[parent_parser])

        self.parser.set_defaults(execute=self.execute)

    def execute(self, args: Namespace):
        print("Generating docs with example constructor...")
        print(f"Input Directory: {args.input_dir}")
        print(f"Output Directory: {args.output_dir}")

        print("Classes found: ", end="")
        pprint([class_data["name"] for class_data in args.ctx["classes"]])


class ExamplePlugin(BasePlugin):

    def register(self, app: AppCommand):
        construct = app.subcommands['construct']

        construct.subcommands["example"] = ExampleCommand()

        construct.subcommands["example"].register(
            construct.subparsers,
            construct.parent_parser
        )
