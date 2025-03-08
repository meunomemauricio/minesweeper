"""Command Line Interface."""

import click
import pyglet

from minesweeper.graphics import MinesweeperWindow


@click.group()
def cli():
    """Pendulum Simulator CLI."""


@cli.command()
def hello():
    MinesweeperWindow()
    pyglet.app.run()
