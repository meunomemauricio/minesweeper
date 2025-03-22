from importlib.metadata import version

from pyglet.text import Label
from pyglet.window import FPSDisplay as PygletFPSDisplay, Window, key

from minesweeper.board import Board
from minesweeper.coordinator import Coordinator
from minesweeper.graphics import LayerMap


class FPSDisplay(PygletFPSDisplay):
    """Custom FPS Display."""

    FONT_SIZE = 16
    FONT_COLOR = 255, 0, 0, 200

    def __init__(self, window: Window):
        super().__init__(window=window)
        self.label = Label(
            font_size=self.FONT_SIZE,
            x=window.width - self.FONT_SIZE * 4,
            y=window.height - self.FONT_SIZE - 1,
            color=self.FONT_COLOR,
            weight="bold",
        )


class MinesweeperWindow(Window):
    CAPTION = f"Minesweeper - v{version('minesweeper')}"

    def __init__(self, board: Board, show_fps: bool) -> None:
        super().__init__(caption=self.CAPTION)
        self._board = board
        self.layers = LayerMap()
        self.coord = Coordinator(board=board, layers=self.layers)
        self.fps_display = FPSDisplay(window=self) if show_fps else None

        # Resize to fit the whole composition
        self.width, self.height = self.coord.width, self.coord.height

    def on_draw(self) -> None:
        """Handle graphics drawing."""
        self.coord.pre_draw()
        self.layers.draw()
        if self.fps_display is not None:
            self.fps_display.draw()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        """Handle Mouse Release events."""
        self.coord.click(x=x, y=y, button=button)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handle Keyboard Release events."""
        match symbol:
            case key.ESCAPE | key.Q:
                self.close()
            case key.R:
                self.coord.reset()
