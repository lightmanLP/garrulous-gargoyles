from .. import structures as struct
from ..entities import Object, Blocking, Collectibles, NonInteractive


class Grass(Object, NonInteractive):
    """Grass object, can be stepped on!"""

    def __init__(self, randomise_size: bool = True, layer: int = -20, **kwargs) -> None:
        super().__init__(
            struct.SPRITES_PATH / "grass" / "grass.png",
            randomise_size=randomise_size,
            **kwargs
        )
        self._layer = layer


class Stone(Object, Collectibles):
    """Stone object, can be stood upon!"""

    def __init__(self, randomise_size: bool = True, layer: int = -20, **kwargs) -> None:
        super().__init__(
            struct.SPRITES_PATH / "stone" / "stone.png",
            randomise_size=randomise_size,
            **kwargs
        )
        self._layer = layer


class Tree(Object, Collectibles, Blocking):
    """Tree object, tall trees can hide you!"""

    def __init__(
            self, size: tuple[int, int] = (150, 150), layer: int = 20, **kwargs
    ) -> None:
        super().__init__(
            struct.SPRITES_PATH / "trees" / "tree.png",
            size=size,
            **kwargs
        )
        self._layer = layer
        self.item = "Fruits"
