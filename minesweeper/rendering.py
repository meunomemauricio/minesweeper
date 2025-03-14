from pathlib import Path

from pyglet import image
from pyglet.graphics import Batch
from pyglet.image import AbstractImage
from pyglet.shapes import BorderedRectangle
from pyglet.text import Label
from pyglet.window import FPSDisplay as PygletFPSDisplay, Window

from minesweeper.board import Board
from minesweeper.cells import StrCell

ASSET_DIR = Path(__name__).parent.parent / "assets"


class BoardDisplay:
    def __init__(self, board: Board, cell_len: int):
        self._board = board
        self._cell_len = cell_len

        self._batch = Batch()

        self._images = self._load_images()

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

    def update(self) -> None:
        """"""

    def draw(self) -> None:
        """"""
        for r in range(0, self._board.rows):
            for c in range(0, self._board.cols):
                cell = self._board[r, c]
                x, y = r * self._cell_len, c * self._cell_len
                self._images[cell.repr].blit(x, y, 0)


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


class CentralTextDisplay:
    FONT_SIZE = 24
    HEIGHT = 50
    WIDTH = 200

    def __init__(self, width: int, height: int, text: str):
        self._batch = Batch()

        self.rect = BorderedRectangle(
            x=(width // 2) - (self.WIDTH // 2),
            y=(height // 2) - (self.HEIGHT // 2),
            width=self.WIDTH,
            height=self.HEIGHT,
            color=(0, 0, 0, 255),
            border_color=(255, 0, 0, 255),
            batch=self._batch,
        )

        self.label = Label(
            font_size=self.FONT_SIZE,
            text=text,
            x=width // 2,
            y=height // 2 + 2,
            anchor_x="center",
            anchor_y="center",
            color=(255, 0, 0, 255),
            weight="bold",
            batch=self._batch,
        )

    def draw(self) -> None:
        self._batch.draw()
