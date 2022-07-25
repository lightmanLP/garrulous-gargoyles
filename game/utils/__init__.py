import random

from .. import structures as struct


def random_position():
    return tuple(map(random.randrange, struct.SCREEN_SIZE))
