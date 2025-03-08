from importlib.metadata import version

from pyglet import window


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
