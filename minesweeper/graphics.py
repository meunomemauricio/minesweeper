from importlib.metadata import version

from pyglet import window

from minesweeper.board import Board
from minesweeper.rendering import BoardDisplay, CentralTextDisplay, FPSDisplay

CELL_LENGTH = 64  # Assume cells are square


class MinesweeperWindow(window.Window):
    CAPTION: str = f"Minesweeper - v{version('minesweeper')}"

    def __init__(self, board: Board, show_fps: bool) -> None:
        self.board = board

        super().__init__(
            width=self.board.rows * CELL_LENGTH,
            height=self.board.cols * CELL_LENGTH,
            caption=self.CAPTION,
        )

        self.board_display = BoardDisplay(board=board, cell_len=CELL_LENGTH)
        self.game_over_text = CentralTextDisplay(
            width=self.width,
            height=self.height,
            text="GAME OVER",
        )
        self.win_text = CentralTextDisplay(
            width=self.width,
            height=self.height,
            text="GG!",
        )
        self.fps_display = FPSDisplay(window=self, is_active=show_fps)

    def _is_out_of_bounds(self, x: float, y: float) -> bool:
        """Check if coordinates are outside the window bounds."""
        return (x < 0 or x >= self.width) or (y < 0 or y >= self.height)

    def _to_board_coords(self, x: float, y: float) -> tuple[int, int]:
        """Convert the window coordinates into board coordinates."""
        return int(x // CELL_LENGTH), int(y // CELL_LENGTH)

    def on_draw(self) -> None:
        """Handle graphics drawing."""
        self.board_display.draw()

        if self.board.has_won:
            self.win_text.draw()

        if self.board.game_over:
            self.game_over_text.draw()

        self.fps_display.draw()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        """Handle Mouse Release events."""
        if self._is_out_of_bounds(x=x, y=y) or self.board.game_over:
            return

        row, col = self._to_board_coords(x=x, y=y)
        match button:
            case window.mouse.LEFT:
                self.board.step(row=row, col=col)
            case window.mouse.RIGHT:
                self.board.flag(row=row, col=col)

        self.board_display.update()

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handle Keyboard Release events."""
        match symbol:
            case window.key.ESCAPE | window.key.Q:
                self.close()
            case window.key.R:
                self.board.reset()

        self.board_display.update()
