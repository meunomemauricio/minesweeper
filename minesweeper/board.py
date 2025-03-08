import random
from typing import Self
from minesweeper.taxonomy import Piece


class Board:

    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols

        self._pieces: list[list[Piece]] = []

    def __getitem__(self, row: int) -> tuple[Piece, ...]:
        """Access the rows of pieces

        This allows for readonly access to the pieces using the format

            board[r][c]
        """
        return self._pieces[row]

    @classmethod
    def random(cls, rows: int, cols: int) -> Self:
        """Generate a board with random pieces.

        Not a valid game, but helps debug the graphics.
        """
        population = [Piece(i) for i in range(1, 13)]

        board = cls(rows=rows, cols=cols)
        board._pieces = [
            random.choices(population=population, k=cols) for _ in range(rows)
        ]
        return board
