from argparse import ArgumentParser, Namespace
from typing import Any
from godocs.cli.command.cli_command import CLICommand
from godocs.cli.command.jinja import JinjaCommand
from godocs.util import module


class ConstructCommand(CLICommand):

    TRANSLATORS = ["rst"]

    parser: ArgumentParser

    subparsers = None

    jinja_command = None

    def register_plugin(self, args: Namespace):
        print(f"Register Plugins: {args}")

        plugin = module.load("construct_plugin", args.construct_plugin)
        register = dict(module.get_functions(plugin))["register"]

        register(self.subparsers)

    def register(self, subparsers: Any):
        self.parser = subparsers.add_parser(
            "construct", help="Construct documentation with a chosen backend")

        self.parser.add_argument(
            "-p", "--plugin",
            dest="construct_plugin",
            help="Optional plugin script path to extend CLI."
        )
        self.parser.add_argument(
            "-t", "--translator",
            default="rst",
            help=f"Which translator to use. Can be one of {self.TRANSLATORS} or a path to a script."
        )

        self.subparsers = self.parser.add_subparsers(
            title="constructor", description="The constructor to use.")

        self.jinja_command = JinjaCommand().register(self.subparsers)
