"""Command Line Interface."""

import click
import pyglet

from minesweeper.board import Board
from minesweeper.graphics import MinesweeperWindow


@click.group()
def cli() -> None:
    """Minesweeper."""


@cli.command()
@click.option("-r", "--rows", type=int, default=10)
@click.option("-c", "--cols", type=int, default=10)
@click.option("-m", "--mines", type=int, default=10)
def run(rows: int, cols: int, mines: int) -> None:
    """Run the Game."""
    board = Board.new(rows=rows, cols=cols, mines=mines)
    MinesweeperWindow(board=board)  # type: ignore[abstract]
    pyglet.app.run()
