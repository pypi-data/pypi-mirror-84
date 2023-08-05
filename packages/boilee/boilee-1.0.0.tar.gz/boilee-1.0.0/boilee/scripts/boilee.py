import click
from rich.pretty import install as use_pretty
from rich.traceback import install as use_rich_traceback

from .make import make
from .run import run


@click.group()
def cli():
    pass


cli.add_command(run)
cli.add_command(make)

use_rich_traceback(extra_lines=4, indent_guides=True)
use_pretty()
