from typing import Literal

from pyglet.graphics import Batch, Group

Layers = Literal["bg", "main", "alert"]


class ToggleGroup(Group):
    """Group Extension class, accepts a visible parameter."""

    def __init__(
        self,
        order: int,
        parent: Group | None = None,
        visible: bool = True,
    ) -> None:
        super().__init__(order=order, parent=parent)
        self.visible = visible

    def hide(self) -> None:
        self.visible = False

    def show(self) -> None:
        self.visible = True


class LayerMap:
    """Combines groups into a single batch for layered rending."""

    def __init__(self) -> None:
        self.batch = Batch()

        self.groups: dict[Layers, ToggleGroup] = {
            "bg": ToggleGroup(order=0),
            "main": ToggleGroup(order=1),
            "alert": ToggleGroup(order=2, visible=False),
        }

    def __getitem__(self, name: Layers) -> ToggleGroup:
        return self.groups[name]

    def draw(self) -> None:
        self.batch.draw()
