from abc import ABC, abstractmethod
from typing import Any
from argparse import ArgumentParser


class CLICommand(ABC):
    """
    Base class that represents a CLI command or subcommand.

    The `register` method should be implemented to connect
    the logic of this command as an `argparse` parser or
    subparser.
    """

    @abstractmethod
    def register(self, subparsers: Any | None = None, parent: ArgumentParser | None = None):
        """
        Abstract method that takes a `subparsers` instance
        (from `argparse.ArgumentParser.add_subparsers`) and
        should append a subparser to them.

        For a root command implementation, the `subparsers`
        parameter may be null, since it isn't a subparser
        as opposed to a main parser.
        """
        pass
