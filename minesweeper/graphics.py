from importlib.metadata import version
from pathlib import Path

from pyglet import image, window
from pyglet.image import AbstractImage

from minesweeper.board import Board, StrCell
from minesweeper.utils import CentralTextDisplay, FPSDisplay

ASSET_DIR = Path(__name__).parent.parent / "assets"
CELL_WIDTH = 64
CELL_HEIGHT = 64


class MinesweeperWindow(window.Window):
    CAPTION: str = f"Minesweeper - v{version('minesweeper')}"

    def __init__(self, board: Board, show_fps: bool) -> None:
        self.board = board

        super().__init__(
            width=self.board.rows * CELL_WIDTH,
            height=self.board.cols * CELL_HEIGHT,
            caption=self.CAPTION,
        )

        self.images = self._load_images()

        self.game_over_text = CentralTextDisplay(self, text="GAME OVER")
        self.fps_display = FPSDisplay(self, is_active=show_fps)

    def _load_images(self) -> dict[StrCell, AbstractImage]:
        return {
            "0": image.load(str(ASSET_DIR / "empty.png")),
            "1": image.load(str(ASSET_DIR / "one.png")),
            "2": image.load(str(ASSET_DIR / "two.png")),
            "3": image.load(str(ASSET_DIR / "three.png")),
            "4": image.load(str(ASSET_DIR / "four.png")),
            "5": image.load(str(ASSET_DIR / "five.png")),
            "6": image.load(str(ASSET_DIR / "six.png")),
            "7": image.load(str(ASSET_DIR / "seven.png")),
            "8": image.load(str(ASSET_DIR / "eight.png")),
            "h": image.load(str(ASSET_DIR / "hidden.png")),
            "m": image.load(str(ASSET_DIR / "mine.png")),
            "f": image.load(str(ASSET_DIR / "flag.png")),
        }

    def _is_out_of_bounds(self, x: float, y: float) -> bool:
        """Check if coordinates are outside the window bounds."""
        return (x < 0 or x >= self.width) or (y < 0 or y >= self.height)

    def _to_board_coords(self, x: float, y: float) -> tuple[int, int]:
        """Convert the window coordinates into board coordinates."""
        return int(x // CELL_WIDTH), int(y // CELL_HEIGHT)

    def on_draw(self) -> None:
        """Handle graphics drawing."""
        for r in range(0, self.board.rows):
            for c in range(0, self.board.cols):
                cell = self.board[r][c]
                x, y = r * CELL_WIDTH, c * CELL_HEIGHT
                self.images[cell.repr()].blit(x, y, 0)

        if self.board.game_over:
            self.game_over_text.draw()

        self.fps_display.draw()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        """Handle Mouse Release events."""
        if button != window.mouse.LEFT:
            return

        if self._is_out_of_bounds(x=x, y=y):
            return

        if not self.board.game_over:
            row, col = self._to_board_coords(x=x, y=y)
            self.board.step(row=row, col=col)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handle Keyboard Release events."""
        if symbol in [window.key.ESCAPE, window.key.Q]:
            self.close()
