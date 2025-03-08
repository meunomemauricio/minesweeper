"""Command Line Interface."""

import click
import pyglet

from minesweeper.graphics import MinesweeperWindow


@click.group()
def cli() -> None:
    """Minesweeper."""


@cli.command()
def run() -> None:
    """Run the Game."""
    MinesweeperWindow()  # type: ignore[abstract]
    pyglet.app.run()
