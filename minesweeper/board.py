import itertools
import random
from typing import Self

from minesweeper.taxonomy import Piece


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

        self._pieces: list[list[Piece]] = []

    def __getitem__(self, row: int) -> tuple[Piece, ...]:
        """Access the rows of pieces

        This allows for readonly access to the pieces using the format

            board[r][c]
        """
        return tuple(self._pieces[row])

    @classmethod
    def random(cls, rows: int, cols: int) -> Self:
        """Generate a board with random pieces.

        Not a valid game, but helps debug the graphics.
        """
        population = [Piece(i) for i in range(0, 12)]

        board = cls(rows=rows, cols=cols, mines=0)
        for _ in range(rows):
            col = random.choices(population=population, k=cols)
            board._pieces.append(col)
            board.mines += len([p for p in col if p == Piece.MINE])

        return board

    @classmethod
    def new(cls, rows: int, cols: int, mines: int) -> Self:
        """Generate a new valid game board."""
        board = cls(rows=rows, cols=cols, mines=mines)
        board._pieces = [(cols * [Piece(0)]) for _ in range(rows)]

        # Randomly distribute the mines
        population = list(itertools.product(range(rows), range(cols)))
        mine_coords = random.sample(population=population, k=mines)
        for r, c in mine_coords:
            board._pieces[r][c] = Piece.MINE

        return board
