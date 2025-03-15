from functools import cached_property
from importlib import resources

from pyglet import resource
from pyglet.image import AbstractImage
from pyglet.shapes import BorderedRectangle
from pyglet.sprite import Sprite
from pyglet.text import Label

from minesweeper.board import Board
from minesweeper.cells import StrCell
from minesweeper.graphics import Canvas

assets_dir = resources.files("minesweeper").joinpath("assets")
with resources.as_file(assets_dir) as assets_path:
    resource.path = [str(assets_path)]
    resource.reindex()


class BoardDisplay:
    def __init__(self, board: Board, cell_len: int, canvas: Canvas):
        self._board = board
        self._cell_len = cell_len
        self._canvas = canvas

        self._sprites: list[list[Sprite]] = self._create_sprites()

    @cached_property
    def _images(self) -> dict[StrCell, AbstractImage]:
        return {
            "0": resource.image("empty.png"),
            "1": resource.image("one.png"),
            "2": resource.image("two.png"),
            "3": resource.image("three.png"),
            "4": resource.image("four.png"),
            "5": resource.image("five.png"),
            "6": resource.image("six.png"),
            "7": resource.image("seven.png"),
            "8": resource.image("eight.png"),
            "h": resource.image("hidden.png"),
            "m": resource.image("mine.png"),
            "f": resource.image("flag.png"),
        }

    def _create_sprites(self) -> list[list[Sprite]]:
        rows = []
        for r in range(0, self._board.rows):
            cols = []
            for c in range(0, self._board.cols):
                x, y = r * self._cell_len, c * self._cell_len
                image = self._images[self._board[r, c].repr]
                cols.append(
                    Sprite(
                        img=image,
                        x=x,
                        y=y,
                        batch=self._canvas.batch,
                        group=self._canvas["main"],
                    )
                )

            rows.append(cols)

        return rows

    def update(self) -> None:
        """Update sprite image to reflect board state"""
        for r in range(0, self._board.rows):
            for c in range(0, self._board.cols):
                cell = self._board[r, c]
                self._sprites[r][c].image = self._images[cell.repr]


class AlertDisplay:
    FONT_SIZE = 24
    HEIGHT = 50
    WIDTH = 200

    def __init__(self, width: int, height: int, text: str, canvas: Canvas):
        self._canvas = canvas

        self.rect = BorderedRectangle(
            x=(width // 2) - (self.WIDTH // 2),
            y=(height // 2) - (self.HEIGHT // 2),
            width=self.WIDTH,
            height=self.HEIGHT,
            color=(0, 0, 0, 255),
            border_color=(255, 0, 0, 255),
            batch=self._canvas.batch,
            group=self._canvas["alert"],
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
            batch=self._canvas.batch,
            group=self._canvas["alert"],
        )

    @property
    def text(self) -> str:
        return self.label.text

    @text.setter
    def text(self, value: str) -> None:
        self.label.text = value
