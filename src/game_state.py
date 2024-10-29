import typing

from src.card import Card
from src.deck import Deck
from src.player import Player


class GameState:
    def __init__(self, players: list[Player], deck: Deck, top: Card, current_player: int = 0, chips: int = 0):
        self.players: list[Player] = players
        self.deck: Deck = deck
        self.top: Card = top
        self.chips = chips
        self._current_player: int = current_player

    def current_player(self) -> Player:
        return self.players[self._current_player]

    def __eq__(self, other):
        if self.players != other.players:
            return False
        if self.deck != other.deck:
            return False
        if self.top != other.top:
            return False
        if self.chips != other.chips:
            return False
        if self._current_player != other._current_player:
            return False
        return True

    def save(self) -> dict:
        return {
          "top": str(self.top),
          "chips": self.chips,
          "deck": str(self.deck),
          "current_player_index": self._current_player,
          "players": [p.save() for p in self.players]
        }

    @classmethod
    def load(cls, data: dict):
        '''
        data = {
            'top': '7',
            'chips': 12,
            'current_player_index': 0,
            'deck': '20 6 10',
            'players': [
                {
                    'name': 'Alex',
                    'hand': '3 8',
                    'score': 11,
                    'chips': 7
                },
                {
                    'name': 'Bob',
                    'hand': '5',
                    'score': 5,
                    'chips': 1
                },
                {
                    'name': 'Charley',
                    'hand': '9 11 21',
                    'score': 41,
                    'chips': 4
                }
            ]
        }
        '''
        players = [Player.load(d) for d in data['players']]

        return cls(
            players=players,
            deck=Deck.load(data['deck']),
            top=Card.load(data['top']),
            chips=data['chips'],
            current_player=int(data['current_player_index']))

    def next_player(self):
        """Ход переходит к следующему игроку."""
        n = len(self.players)
        self._current_player = (self._current_player + 1) % n

    def draw_card(self):
        """Текущий игрок берет карту из колоды."""
        card = self.deck.draw_card()
        self.current_player().hand.add_card(card)

    def take_card(self):
        """Взять карту и фишки."""
        self.current_player().hand.add_card(self.top)
        self.current_player().chips += self.chips

    def to_pay(self):
        """Заплатить фишкой."""
        self.current_player().chips *= 100
        self.chips +=1
        self.next_player()

    def score_players(self):
        """Очки игроков"""
        return {p.name: p.score-p.chips for p in self.players}

