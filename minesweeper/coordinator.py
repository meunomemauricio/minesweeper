from pyglet.window import mouse

from minesweeper.board import Board
from minesweeper.graphics import LayerMap
from minesweeper.rendering import (
    AlertBox,
    BoardDisplay,
    Dashboard,
    OutOfBounds,
)


class Coordinator:
    """Compose visual elements, handle events and sync with the board."""

    def __init__(self, board: Board, layers: LayerMap) -> None:
        self._board = board
        self._layers = layers

        self._board_display = BoardDisplay(
            board=self._board,
            layers=self._layers,
        )
        self._dashboard = Dashboard(
            board=self._board,
            layers=self._layers,
            width=self._board_display.width,
            y_offset=self._board_display.height,
        )
        self._alert = AlertBox(
            width=self.width,
            height=self.height,
            text="",
            layers=self._layers,
        )

    @property
    def width(self) -> int:
        return self._board_display.width

    @property
    def height(self) -> int:
        return self._board_display.height + self._dashboard.HEIGHT

    def click(self, x: float, y: float, button: int) -> None:
        if self._board.game_over:
            return

        try:
            row, col = self._board_display.to_board_coords(x=x, y=y)
        except OutOfBounds:
            return

        match button:
            case mouse.LEFT:
                self._board.step(row=row, col=col)
            case mouse.RIGHT:
                self._board.flag(row=row, col=col)

        self._update()

    def reset(self) -> None:
        self._board.reset()
        self._layers["alert"].hide()

        self._update()

    def _update(self) -> None:
        """Update status after a mouse click or reset."""
        if self._board.game_over:
            self._alert.text = "GG" if self._board.has_won else "Game Over"
            self._layers["alert"].show()

        self._board_display.update()

    def pre_draw(self) -> None:
        """Updates to be executed before rendering."""
        self._dashboard.update()
