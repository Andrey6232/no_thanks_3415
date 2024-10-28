from abc import ABC, abstractmethod

from src.player import Player


class PlayerInteraction(ABC):
    @classmethod
    @abstractmethod
    def choose_action(cls):
        """
        Принимает решение взять карту или положить фишку.
        """
        pass

    @classmethod
    def inform_player_takes_card(cls, player: Player):
        """
        Сообщает, что игрок взял карту.
        """
        pass

    @classmethod
    def inform_card_to_pay(cls, player: Player):
        """
        Сообщает, что игрок использовал фишку.
        """
        pass