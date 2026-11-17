from importlib.resources import files

import click
from packaging.version import Version

from soupdemo import __version__

Version("1.0")


def greeting(name: str) -> str:
    template = files("soupdemo").joinpath("data/greeting.txt").read_text(encoding="utf-8")
    return template.strip().format(name=name)


@click.command()
@click.option("--name", default="world", help="Person to greet.")
@click.version_option(version=__version__)
def main(name: str) -> None:
    """Print a greeting from an installed package resource."""
    click.echo(greeting(name))
