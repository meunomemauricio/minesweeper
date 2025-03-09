from dataclasses import dataclass


@dataclass
class Cell:
    MAX_COUNT = 8

    is_hidden: bool = True
    is_flag: bool = False
    is_mine: bool = False
    count: int = 0  # Adjacent Mines

    def __repr__(self) -> str:
        """String representation of the cell."""
        if self.is_flag:
            return "f"

        if self.is_hidden:
            return "h"

        if self.is_mine:
            return "m"

        return str(self.count)


# List of meaningful Cell states, to help with random generation.
CELL_POPULATION: list[Cell] = [
    Cell(is_hidden=True),
    Cell(is_hidden=False, count=0),
    Cell(is_hidden=False, count=1),
    Cell(is_hidden=False, count=2),
    Cell(is_hidden=False, count=3),
    Cell(is_hidden=False, count=4),
    Cell(is_hidden=False, count=5),
    Cell(is_hidden=False, count=6),
    Cell(is_hidden=False, count=7),
    Cell(is_hidden=False, count=8),
    Cell(is_hidden=False, count=0),
    Cell(is_hidden=False, is_flag=True),
    Cell(is_hidden=False, is_mine=True),
]
