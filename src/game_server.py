import inspect
import json
import sys

from src.deck import Deck
from src.game_state import GameState
from src.hand import Hand
from src.player import Player
from src.player_interaction import PlayerInteraction
import src.player_interactions as all_player_types

import logging

import enum


class GamePhase(enum.StrEnum):
    DRAW_EXTRA = "Draw extra card"
    BIDDING = "Choose to pay or take card"
    DECLARE_WINNER = "Declare a winner"
    GAME_END = "Game ended"

class GameServer:

    def __init__(self, player_types, game_state):
        self.game_state: GameState = game_state
        self.player_types: dict = player_types  # {player: PlayerInteractions}

    @classmethod
    def load_game(cls):
        # TODO: выбрать имя файла
        filename = 'uno.json'
        with open(filename, 'r') as fin:
            data = json.load(fin)
            game_state = GameState.load(data)
            print(game_state.save())
            player_types = {}
            for player, player_data in zip(game_state.players, data['players']):
                kind = player_data['kind']
                kind = getattr(all_player_types, kind)
                player_types[player] = kind
            return GameServer(player_types=player_types, game_state=game_state)

    def save(self):
        filename = 'no_thanks.json'
        data = self.save_to_dict()
        with open(filename, 'w') as fout:
            json.dump(data, fout, indent=4)

    def save_to_dict(self):
        # {'top': '7', 'chips': 12, 'current_player_index': 1, 'deck': '20 6 10', 'players': [{'name': 'Alex', 'hand': '3 8', 'score': 5, 'chips': 7}, {'name': 'Bob', 'hand': '5', 'score': 1, 'chips': 1}, {'name': 'Charley', 'hand': '9 11 21', 'score': 3, 'chips': 4}]}
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            player_interaction = self.player_types[player]
            data['players'][player_index]['kind'] = self.player_types[player].__name__
        return data

    @classmethod
    def get_players(cls):
        player_count = cls.request_player_count()

        player_types = {}
        for p in range(player_count):
            name, kind = cls.request_player()
            player = Player(name, Hand())
            player_types[player] = kind
        return player_types

    @classmethod
    def new_game(cls, player_types: dict):
        deck = Deck(None).shuffle()
        for _ in range(9):
            deck.draw_card()

        top = deck.draw_card()
        game_state = GameState(list(player_types.keys()), deck, top)

        print(game_state.save())

        res = cls(player_types, game_state)
        return res

    def run(self):
        current_phase = GamePhase.BIDDING
        while current_phase != GamePhase.GAME_END:
            phases = {
                GamePhase.DRAW_EXTRA: self.draw_extra,
                GamePhase.BIDDING: self.bidding_phase,
                GamePhase.DECLARE_WINNER: self.declare_winner_phase
            }
            current_phase = phases[current_phase]()

    def declare_winner_phase(self) -> GamePhase:
        print(f"{self.game_state.current_player()} is the winner!")
        return GamePhase.GAME_END

    def bidding_phase(self):
        pass

    def draw_extra(self):
        pass

    def inform_all(self):
        pass

    @staticmethod
    def request_player_count() -> int:
        pass

    @staticmethod
    def request_player() -> (str, PlayerInteraction):
        pass

def __main__():
    pass

if __name__ == "__main__":
    __main__()



