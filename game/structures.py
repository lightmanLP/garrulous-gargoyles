from enum import IntEnum

SCREEN_SIZE = (1080, 720)


class Color(IntEnum):
    RED = 0xFF0000
    GREEN = 0x00FF00
    BLUE = 0x0000FF
    WHITE = 0xFFFFFF
    BLACK = 0x000000

    @property
    def rgba(self) -> int:
        return (self.value << 8) + 0xFF
