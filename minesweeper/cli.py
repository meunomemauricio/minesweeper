"""Command Line Interface."""

import click
import pyglet

from minesweeper.board import Board
from minesweeper.graphics import MinesweeperWindow


@click.group()
def cli() -> None:
    """Minesweeper."""


@cli.command()
def run() -> None:
    """Run the Game."""
    board = Board.random(10, 10)
    MinesweeperWindow(board=board)  # type: ignore[abstract]
    pyglet.app.run()
