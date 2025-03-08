"""Command Line Interface."""

import click


@click.group()
def cli():
    """Pendulum Simulator CLI."""


@cli.command()
def hello():
    print("Hello World!")
