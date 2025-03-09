from enum import IntEnum


class Piece(IntEnum):
    """Board Pieces."""

    EMPTY = 0

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8

    BASE = 9
    MINE = 10
    FLAG = 11
