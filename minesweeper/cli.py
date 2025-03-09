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
@click.option("-F", "--fps/--no-fps", type=bool, default=False)
def run(rows: int, cols: int, mines: int, fps: bool) -> None:
    """Run the Game."""
    board = Board(rows=rows, cols=cols, mines=mines)
    MinesweeperWindow(board=board, show_fps=fps)  # type: ignore[abstract]
    pyglet.app.run()
