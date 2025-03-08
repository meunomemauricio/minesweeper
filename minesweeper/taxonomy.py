from enum import IntEnum

class Piece(IntEnum):
    """Board Pieces."""
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8

    BASE = 9
    BOMB = 10
    FLAG = 11
    EMPTY = 12