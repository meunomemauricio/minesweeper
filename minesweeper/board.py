import itertools
import random
from dataclasses import dataclass
from typing import Literal, get_args

from typing_extensions import TypeIs

StrCell = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "f", "h", "m"]
VALID_COUNT: frozenset[StrCell] = frozenset(get_args(StrCell))


class GameOverError(Exception):
    """Tried to execute an action after the game is over."""


@dataclass
class Cell:
    MAX_COUNT = 8

    is_hidden: bool = True
    is_flag: bool = False
    is_mine: bool = False
    count: int = 0  # Adjacent Mines

    def _is_str_cell(self, val: str) -> TypeIs[StrCell]:
        """Type Narrowing Check."""
        return val in VALID_COUNT

    def repr(self) -> StrCell:
        """String representation of the cell."""
        value = ""
        match (self.is_flag, self.is_hidden, self.is_mine):
            case (True, _, _):
                value = "f"
            case (False, True, _):
                value = "h"
            case (False, False, True):
                value = "m"
            case (False, False, False):
                value = str(self.count)

        assert self._is_str_cell(val=value), f"Unexpected value: {value}"
        return value


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

        self._cells = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

        self.initialized = False
        self.game_over = False

    def __getitem__(self, row: int) -> tuple[Cell, ...]:
        """Access the rows of pieces

        This allows for readonly access to the cells using the format

            board[r][c]
        """
        return tuple(self._cells[row])

    def _initialize(self, row: int, col: int) -> None:
        """Generate a new valid game board.

        `row` and `col` are the coordinates of the first step.
        """
        # Generate possible mine coordinates, making sure the first step is
        # removed.
        population = list(itertools.product(range(self.rows), range(self.cols)))
        population.remove((row, col))

        # Assign mines at random
        mine_coords = random.sample(population=population, k=self.mines)
        for r_m, c_m in mine_coords:
            self._cells[r_m][c_m].is_mine = True

            # Increment adjacent regular cells
            for i, j in itertools.product(range(-1, 2), range(-1, 2)):
                try:
                    cell = self._cells[r_m + i][c_m + j]
                except IndexError:
                    pass
                else:
                    if cell.count < Cell.MAX_COUNT:
                        self._cells[r_m + i][c_m + j].count += 1

        self.initialized = True

    def step(self, row: int, col: int) -> None:
        """Step into one of the cells.

        The board is initialized on the first step as a way to ensure it's not
        on a mine straight away.
        """
        if not (self.initialized):
            self._initialize(row=row, col=col)

        if self.game_over:
            raise GameOverError("Can't step after game over.")

        cell = self._cells[row][col]
        cell.is_hidden = False

        if cell.is_mine:
            self.game_over = True
