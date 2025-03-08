from pathlib import Path
from importlib.metadata import version
import random

from pyglet import window, image
from pyglet.image import AbstractImage

from minesweeper.taxonomy import Piece


ASSET_DIR = Path(__name__).parent.parent / "assets"

class MinesweeperWindow(window.Window):
    CAPTION: str = f"Minesweeper - v{version('minesweeper')}"
    WIDTH = 800
    HEIGHT = 600

    def __init__(self) -> None:
        super().__init__(
            width=self.WIDTH,
            height=self.HEIGHT,
            caption=self.CAPTION,
        )

        self.images = self.load_images()

        self.pause = False

    def load_images(self) -> dict[Piece, AbstractImage]:
        board_dir = ASSET_DIR / "board"
        return {
            Piece.BASE: image.load(str(board_dir / "base.png")),
            Piece.BOMB: image.load(str(board_dir / "bomb.png")),
            Piece.ONE: image.load(str(board_dir / "one.png")),
            Piece.TWO: image.load(str(board_dir / "two.png")),
            Piece.THREE: image.load(str(board_dir / "three.png")),
            Piece.FOUR: image.load(str(board_dir / "four.png")),
            Piece.FIVE: image.load(str(board_dir / "five.png")),
            Piece.SIX: image.load(str(board_dir / "six.png")),
            Piece.SEVEN: image.load(str(board_dir / "seven.png")),
            Piece.EIGHT: image.load(str(board_dir / "eight.png")),
            Piece.EMPTY: image.load(str(board_dir / "empty.png")),
            Piece.FLAG: image.load(str(board_dir / "flag.png")),
        }

    def on_draw(self):
        if not self.pause:
            for x in range(0, self.WIDTH - 64, 64):
                for y in range(0, self.HEIGHT - 64, 64):
                    piece = random.choice(range(1, 13))
                    self.images[piece].blit(x, y, 0)

            self.pause = True