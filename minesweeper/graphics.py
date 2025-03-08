import random
from importlib.metadata import version
from pathlib import Path

from pyglet import image, window
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
        return {
            Piece.BASE: image.load(str(ASSET_DIR / "base.png")),
            Piece.BOMB: image.load(str(ASSET_DIR / "bomb.png")),
            Piece.ONE: image.load(str(ASSET_DIR / "one.png")),
            Piece.TWO: image.load(str(ASSET_DIR / "two.png")),
            Piece.THREE: image.load(str(ASSET_DIR / "three.png")),
            Piece.FOUR: image.load(str(ASSET_DIR / "four.png")),
            Piece.FIVE: image.load(str(ASSET_DIR / "five.png")),
            Piece.SIX: image.load(str(ASSET_DIR / "six.png")),
            Piece.SEVEN: image.load(str(ASSET_DIR / "seven.png")),
            Piece.EIGHT: image.load(str(ASSET_DIR / "eight.png")),
            Piece.EMPTY: image.load(str(ASSET_DIR / "empty.png")),
            Piece.FLAG: image.load(str(ASSET_DIR / "flag.png")),
        }

    def on_draw(self) -> None:
        if not self.pause:
            for x in range(0, self.WIDTH - 64, 64):
                for y in range(0, self.HEIGHT - 64, 64):
                    piece = Piece(random.choice(range(1, 13)))
                    self.images[piece].blit(x, y, 0)

            self.pause = True
