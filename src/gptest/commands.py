import click
import sys
import os
import glob
from .core import Core
from . import constants


class Mash(object):
    pass


@click.group(invoke_without_command=True)
@click.option("--debug/--no-debug", default=False, help="enable debug logging")
@click.option(
    "--version/--no-version", "-v", default=False, help="show version. (default: False)"
)
@click.pass_context
def cli(ctx, debug, version):
    ctx.obj = Mash()
    ctx.obj.debug = debug
    if version:
        print(constants.VERSION)
        sys.exit()

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(help="Specify source path")
@click.option(
    "--sources", "-s", required=True, multiple=True
)
@click.option(
    "--output", "-o", required=True
)
@click.option(
    "--extension", "-e", default=constants.DEFAULT_PYTHON_EXTENSION
)
@click.pass_context
def python(ctx, sources, output, extension):
    core = Core(ctx.obj.debug, output)

    for source in sources:
        if os.path.isdir(source):
            glob_string = f"{source}/**/*.{extension}"
            paths = glob.glob(glob_string, recursive=True)
            for path in paths:
                code = core.generate_test_code(path)

        elif os.path.isfile(source):
            code = core.generate_test_code(source)


def main():
    cli(obj={})
