from functools import cached_property
from importlib import resources

from pyglet import resource
from pyglet.image import AbstractImage
from pyglet.shapes import BorderedRectangle
from pyglet.sprite import Sprite
from pyglet.text import Label

from minesweeper.board import Board
from minesweeper.cells import StrCell
from minesweeper.graphics import LayerMap

assets_dir = resources.files("minesweeper").joinpath("assets")
with resources.as_file(assets_dir) as assets_path:
    resource.path = [str(assets_path)]
    resource.reindex()


class OutOfBounds(Exception):
    """Received event coordinates outside of the board area."""


class Composition:
    CELL_LENGTH = 64  # Assume cells are square

    _alert: "AlertBox"
    _board_display: "BoardDisplay"

    def __init__(self, board: Board, layers: LayerMap) -> None:
        self._board = board
        self._layers = layers

        self._board_display = BoardDisplay(
            board=self._board,
            cell_len=self.CELL_LENGTH,
            layers=self._layers,
        )
        self._alert = AlertBox(
            width=self.width,
            height=self.height,
            text="",
            layers=self._layers,
        )

    @property
    def width(self) -> int:
        return self._board.rows * self.CELL_LENGTH

    @property
    def height(self) -> int:
        return self._board.cols * self.CELL_LENGTH

    def to_board_coords(self, x: float, y: float) -> tuple[int, int]:
        """Convert window coordinates into board coordinates."""
        if self._is_out_of_bounds(x=x, y=y):
            raise OutOfBounds("Outside board area")

        return int(x // self.CELL_LENGTH), int(y // self.CELL_LENGTH)

    def _is_out_of_bounds(self, x: float, y: float) -> bool:
        """Check if coordinates are outside the window bounds.

        This usually happens when clicking inside the window and releasing
        outside.
        """
        return (x < 0 or x >= self.width) or (y < 0 or y >= self.height)

    def update(self) -> None:
        if self._board.has_won:
            self._alert.text = "GG!"
            self._layers["alert"].show()

        if self._board.game_over:
            self._alert.text = "Game Over"
            self._layers["alert"].show()

        self._board_display.update()


class BoardDisplay:
    def __init__(self, board: Board, cell_len: int, layers: LayerMap) -> None:
        self._board = board
        self._cell_len = cell_len
        self.layers = layers

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
                        batch=self.layers.batch,
                        group=self.layers["main"],
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


class AlertBox:
    FONT_SIZE = 24
    HEIGHT = 50
    WIDTH = 200

    def __init__(self, width: int, height: int, text: str, layers: LayerMap):
        self._layers = layers

        self.rect = BorderedRectangle(
            x=(width // 2) - (self.WIDTH // 2),
            y=(height // 2) - (self.HEIGHT // 2),
            width=self.WIDTH,
            height=self.HEIGHT,
            color=(0, 0, 0, 255),
            border_color=(255, 0, 0, 255),
            batch=self._layers.batch,
            group=self._layers["alert"],
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
            batch=self._layers.batch,
            group=self._layers["alert"],
        )

    @property
    def text(self) -> str:
        return self.label.text

    @text.setter
    def text(self, value: str) -> None:
        self.label.text = value
