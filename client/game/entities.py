from .. import structures as struct
from ..entities import Blocking, Collectible, Object


class Grass(Object):
    """Grass object, can be stepped on!"""

    PATH = struct.SPRITES_PATH / "grass" / "grass.png"

    def __init__(self, randomise_size: bool = True, layer: int = -20, **kwargs) -> None:
        super().__init__(randomise_size=randomise_size, layer=layer, **kwargs)


class Stone(Object, Collectible):
    """Stone object, can be stood upon!"""

    PATH = struct.SPRITES_PATH / "stone" / "stone.png"
    item = "stone"

    def __init__(self, randomise_size: bool = True, layer: int = -20, **kwargs) -> None:
        super().__init__(randomise_size=randomise_size, layer=layer, **kwargs)


class Tree(Object, Collectible, Blocking):
    """Tree object, tall trees can hide you!"""

    PATH = struct.SPRITES_PATH / "trees" / "tree.png"
    item = "fruits"

    def __init__(self, size: tuple[int, int] = (150, 150), layer: int = 20, **kwargs) -> None:
        super().__init__(size=size, layer=layer, **kwargs)
