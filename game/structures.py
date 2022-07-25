from enum import IntEnum

SCREEN_SIZE = (1080, 720)
WIDTH, HEIGHT = SCREEN_SIZE
CENTER = WIDTH//2, HEIGHT//2


class Color(IntEnum):
    RED = 0xFF0000
    GREEN = 0x00FF00
    BLUE = 0x0000FF
    WHITE = 0xFFFFFF
    BLACK = 0x000000
    BACKGROUND = 0x4caf4f

    @property
    def rgba(self) -> int:
        return (self.value << 8) + 0xFF
