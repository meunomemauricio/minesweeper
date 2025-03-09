from importlib.metadata import version
from pathlib import Path

from pyglet import image, window
from pyglet.image import AbstractImage

from minesweeper.board import Board

ASSET_DIR = Path(__name__).parent.parent / "assets"
CELL_WIDTH = 64
CELL_HEIGHT = 64


class MinesweeperWindow(window.Window):
    CAPTION: str = f"Minesweeper - v{version('minesweeper')}"

    def __init__(self, board: Board) -> None:
        self.board = board

        super().__init__(
            width=self.board.rows * CELL_WIDTH,
            height=self.board.cols * CELL_HEIGHT,
            caption=self.CAPTION,
        )

        self.images = self.load_images()

        self.pause = False

    def load_images(self) -> dict[str, AbstractImage]:
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

    def on_draw(self) -> None:
        if not self.pause:
            for r in range(0, self.board.rows):
                for c in range(0, self.board.cols):
                    cell = self.board[r][c]
                    x, y = r * CELL_WIDTH, c * CELL_HEIGHT
                    self.images[repr(cell)].blit(x, y, 0)

            self.pause = True

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol in [window.key.ESCAPE, window.key.Q]:
            self.close()
