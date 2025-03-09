import itertools
import random
from typing import Self

from minesweeper.cells import CELL_POPULATION, Cell


class GameOverError(Exception):
    """Tried to execute an action after the game is over."""


class Board:
    # Maximum allowed mines as a fraction of the total # of cells
    MAX_MINES = 0.5

    def __init__(self, rows: int, cols: int, mines: int) -> None:
        max_mines = int((rows * cols) * self.MAX_MINES)
        if mines > max_mines:
            raise ValueError(f"Too many mines (max. {max_mines})")

        self.rows = rows
        self.cols = cols
        self.mines = mines

        self._cells: list[list[Cell]] = []

        self.game_over = False

    def __getitem__(self, row: int) -> tuple[Cell, ...]:
        """Access the rows of pieces

        This allows for readonly access to the cells using the format

            board[r][c]
        """
        return tuple(self._cells[row])

    @classmethod
    def random(cls, rows: int, cols: int) -> Self:
        """Generate a board with random pieces.

        Not a valid game, but helps debug the graphics.
        """
        board = cls(rows=rows, cols=cols, mines=0)
        for _ in range(rows):
            col = random.choices(population=CELL_POPULATION, k=cols)
            board._cells.append(col)
            board.mines += len([p for p in col if p == p.is_mine])

        return board

    @classmethod
    def new(cls, rows: int, cols: int, mines: int) -> Self:
        """Generate a new valid game board."""
        board = cls(rows=rows, cols=cols, mines=mines)
        board._cells = [[Cell() for _ in range(cols)] for _ in range(rows)]

        # Randomly assign mines
        population = list(itertools.product(range(rows), range(cols)))
        mine_coords = random.sample(population=population, k=mines)
        for r_m, c_m in mine_coords:
            board._cells[r_m][c_m].is_mine = True

            # Increment adjacent regular cells
            for i, j in itertools.product(range(-1, 2), range(-1, 2)):
                try:
                    cell = board._cells[r_m + i][c_m + j]
                except IndexError:
                    pass
                else:
                    if cell.count < Cell.MAX_COUNT:
                        board._cells[r_m + i][c_m + j].count += 1

        return board

    def step(self, row: int, col: int) -> None:
        """Step into one of the cells."""
        if self.game_over:
            raise GameOverError("Can't step after game over.")

        cell = self._cells[row][col]
        cell.is_hidden = False

        if cell.is_mine:
            self.game_over = True
