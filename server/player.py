import hashlib
import random


class Player:
    """Store data about players"""

    def __init__(self, name: str):
        self.name: str = name
        salt = random.randbytes(16)
        self.id = hashlib.md5(salt + name.encode()).hexdigest()
