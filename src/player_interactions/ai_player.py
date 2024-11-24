from src.player import Player
from src.player_interaction import PlayerInteraction
import random


class Bot(PlayerInteraction):
    @classmethod
    def choose_action(cls, player: Player):
        if player.chips > 0:
            return random.choice(['Take card', 'Spend'])
        else:
            return 'Take card'

    @classmethod
    def inform_card_take(cls, player: Player):
        """
        Сообщает, что игрок взял карту
        """
        pass

    @classmethod
    def inform_card_to_pay(cls, player: Player):
        """
        Сообщает, что игрок использовал фишку
        """
        pass