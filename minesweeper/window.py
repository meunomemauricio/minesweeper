from importlib.metadata import version

from pyglet.text import Label
from pyglet.window import FPSDisplay as PygletFPSDisplay, Window, key, mouse

from minesweeper.board import Board
from minesweeper.graphics import Canvas
from minesweeper.rendering import AlertDisplay, BoardDisplay


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
    CELL_LENGTH = 64  # Assume cells are square

    def __init__(self, board: Board, show_fps: bool) -> None:
        self.board = board

        super().__init__(
            width=self.board.rows * self.CELL_LENGTH,
            height=self.board.cols * self.CELL_LENGTH,
            caption=self.CAPTION,
        )

        self.canvas = Canvas()

        self.board_display = BoardDisplay(
            board=board,
            cell_len=self.CELL_LENGTH,
            canvas=self.canvas,
        )
        self.alert = AlertDisplay(
            width=self.width,
            height=self.height,
            text="GAME OVER",
            canvas=self.canvas,
        )
        self.fps_display = FPSDisplay(window=self, is_active=show_fps)

    def on_draw(self) -> None:
        """Handle graphics drawing."""
        self.canvas.draw()
        self.fps_display.draw()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        """Handle Mouse Release events."""
        if self._is_out_of_bounds(x=x, y=y) or self.board.game_over:
            return

        row, col = self._to_board_coords(x=x, y=y)
        match button:
            case mouse.LEFT:
                self.board.step(row=row, col=col)
            case mouse.RIGHT:
                self.board.flag(row=row, col=col)

        self._update_state()

    def _is_out_of_bounds(self, x: float, y: float) -> bool:
        """Check if coordinates are outside the board bounds."""
        return (x < 0 or x >= self.width) or (y < 0 or y >= self.height)

    def _to_board_coords(self, x: float, y: float) -> tuple[int, int]:
        """Convert the window coordinates into board coordinates."""
        return int(x // self.CELL_LENGTH), int(y // self.CELL_LENGTH)

    def _update_state(self) -> None:
        if self.board.has_won:
            self.alert.text = "GG!"
            self.canvas["alert"].show()

        if self.board.game_over:
            self.alert.text = "Game Over"
            self.canvas["alert"].show()

        self.board_display.update()

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handle Keyboard Release events."""
        match symbol:
            case key.ESCAPE | key.Q:
                self.close()
            case key.R:
                self.board.reset()
                self.canvas["alert"].hide()

        self._update_state()
