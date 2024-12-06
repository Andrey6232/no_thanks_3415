from src.player import Player
from src.player_interaction import PlayerInteraction
import random


class Bot(PlayerInteraction):
    @classmethod
    def choose_action(cls, player: Player):
        if player.chips > 0:
            return random.choice(['Take card', 'Spend'])
        return 'Take card'