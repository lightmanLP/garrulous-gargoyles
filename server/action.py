from .player import Player


class Action:  # lawsuit
    def __init__(self, player: Player, action_type, target=None):
        self.player = player
        self.target = target
        self.type = action_type
