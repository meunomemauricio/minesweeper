from importlib.metadata import version

from pyglet.text import Label
from pyglet.window import FPSDisplay as PygletFPSDisplay, Window, key, mouse

from minesweeper.board import Board
from minesweeper.graphics import LayerMap
from minesweeper.rendering import Composition, OutOfBounds


class FPSDisplay(PygletFPSDisplay):
    """Custom FPS Display."""

    FONT_SIZE = 16
    FONT_COLOR = 255, 0, 0, 200

    def __init__(self, window: Window, is_active: bool = True):
        super().__init__(window=window)
        self._is_active = is_active

        self.label = Label(
            font_size=self.FONT_SIZE,
            x=window.width - self.FONT_SIZE * 4,
            y=window.height - self.FONT_SIZE - 1,
            color=self.FONT_COLOR,
            weight="bold",
        )

    def update(self) -> None:
        if self._is_active:
            super().update()

    def draw(self) -> None:
        if self._is_active:
            super().draw()


class MinesweeperWindow(Window):
    CAPTION = f"Minesweeper - v{version('minesweeper')}"

    def __init__(self, board: Board, show_fps: bool) -> None:
        super().__init__(caption=self.CAPTION)

        self._board = board
        self.layers = LayerMap()
        self.comp = Composition(board=board, layers=self.layers)
        self.fps_display = FPSDisplay(window=self, is_active=show_fps)

        # Resize to fit the composition
        self.width, self.height = self.comp.width, self.comp.height

    def on_draw(self) -> None:
        """Handle graphics drawing."""
        self.layers.draw()
        self.fps_display.draw()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        """Handle Mouse Release events."""
        if self._board.game_over:
            return

        try:
            row, col = self.comp.to_board_coords(x=x, y=y)
        except OutOfBounds:
            return

        match button:
            case mouse.LEFT:
                self._board.step(row=row, col=col)
            case mouse.RIGHT:
                self._board.flag(row=row, col=col)

        self.comp.update()

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handle Keyboard Release events."""
        match symbol:
            case key.ESCAPE | key.Q:
                self.close()
            case key.R:
                self._board.reset()
                self.layers["alert"].hide()

        self.comp.update()
