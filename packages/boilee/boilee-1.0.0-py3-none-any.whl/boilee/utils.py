import sys

from rich.console import Console


def exit_with_error(message: str, **args):
    console = Console()

    console.print(message, **args)

    sys.exit(1)
