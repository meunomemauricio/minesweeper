from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, get_args

if TYPE_CHECKING:
    from typing_extensions import TypeIs


StrCell = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "f", "h", "m"]
VALID_COUNT: frozenset[StrCell] = frozenset(get_args(StrCell))


@dataclass
class Cell:
    MAX_COUNT = 8

    row: int
    col: int

    is_hidden: bool = True
    is_flag: bool = False
    is_mine: bool = False
    count: int = 0  # Adjacent Mines

    def __hash__(self) -> int:
        """Allows for storing Cells in a Set."""
        return hash((self.row, self.col))

    def _is_str_cell(self, val: str) -> "TypeIs[StrCell]":
        """Type Narrowing Check."""
        return val in VALID_COUNT

    @property
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

    @property
    def is_empty(self) -> bool:
        """Whether the cell has no adjacent mines."""
        if self.is_mine or self.is_flag or self.count:
            return False

        return self.count == 0

    @property
    def is_correct(self) -> bool:
        """If the cell is a correctly flagged mine.

        This state is kept secret from the player.
        """
        return self.is_flag and self.is_mine


class CellMatrix:
    """Strict List - Doesn't wrap around negative indices."""

    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols

        self._matrix: list[list[Cell]] = [
            [Cell(r, c) for c in range(self.cols)] for r in range(self.rows)
        ]

    def __getitem__(self, coord: tuple[int, int]) -> Cell:
        if coord[0] < 0 or coord[1] < 0:
            raise IndexError("Negative index access is not allowed")

        return self._matrix[coord[0]][coord[1]]

    @property
    def hidden_count(self) -> int:
        return sum(sum(1 for cell in row if cell.is_hidden) for row in self._matrix)

    @property
    def correct_count(self) -> int:
        return sum(sum(1 for cell in row if cell.is_correct) for row in self._matrix)
