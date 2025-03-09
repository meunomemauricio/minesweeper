from pyglet.graphics import Batch
from pyglet.shapes import BorderedRectangle
from pyglet.text import Label
from pyglet.window import FPSDisplay as PygletFPSDisplay, Window


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

    def draw(self) -> None:
        if self._is_active:
            super().draw()


class CentralTextDisplay:
    FONT_SIZE = 24
    HEIGHT = 50
    WIDTH = 200

    def __init__(self, window: Window, text: str):
        self._batch = Batch()

        self.rect = BorderedRectangle(
            x=(window.width // 2) - (self.WIDTH // 2),
            y=(window.height // 2) - (self.HEIGHT // 2),
            width=self.WIDTH,
            height=self.HEIGHT,
            color=(0, 0, 0, 255),
            border_color=(255, 0, 0, 255),
            batch=self._batch,
        )

        self.label = Label(
            font_size=self.FONT_SIZE,
            text=text,
            x=window.width // 2,
            y=window.height // 2 + 2,
            anchor_x="center",
            anchor_y="center",
            color=(255, 0, 0, 255),
            weight="bold",
            batch=self._batch,
        )

    def draw(self) -> None:
        self._batch.draw()
