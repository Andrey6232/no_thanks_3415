import inspect
import json


from src.deck import Deck
from src.game_state import GameState
from src.hand import Hand
from src.player import Player
from src.player_interaction import PlayerInteraction
import src.player_interactions as all_player_types



import enum


class GamePhase(enum.StrEnum):
    START_BIDDING = "Draw extra card"
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
                GamePhase.START_BIDDING: self.start_bidding_phase,
                GamePhase.BIDDING: self.bidding_phase,
                GamePhase.DECLARE_WINNER: self.declare_winner_phase
            }
            current_phase = phases[current_phase]()

    def declare_winner_phase(self) -> GamePhase:
        score = self.game_state.score_players()
        winner = min(score, key=lambda k: score[k])
        print(f"{winner, score[winner]} is the winner!")
        return GamePhase.GAME_END

    def start_bidding_phase(self):
        if self.game_state.deck == Deck([]):
            return GamePhase.DECLARE_WINNER
        self.game_state.card = self.game_state.deck.draw_card()
        self.game_state.score = 0
        print('Top:', {"card": self.game_state.card, "score": self.game_state.score})
        return GamePhase.BIDDING

    def bidding_phase(self):
        current_player = self.game_state.current_player()
        interaction = self.player_types[current_player.name]
        choose = interaction.choose_action(current_player, self.game_state.chips)
        if choose == 'Take card':
            self.game_state.take_card()
            interaction.inform_card_take(current_player)
            return GamePhase.START_BIDDING
        elif choose == 'Spend':
            self.game_state.to_pay()
            interaction.inform_player_spend(current_player)
            self.game_state.next_player()
            return GamePhase.BIDDING

    def inform_all(self, method: str, *args, **kwargs):
        for p in self.player_types.values():
            getattr(p, method)(*args, **kwargs)

    @staticmethod
    def request_player_count() -> int:
        while True:
            try:
                player_count = int(input('How many players?\n'))
                if 3 <= player_count <= 5:
                    return player_count
            except ValueError:
                pass
            print('Please input a number between 3 and 5')

    @staticmethod
    def request_player() -> (str, PlayerInteraction):
        player_types = []
        for name, cls in inspect.getmembers(all_player_types):
            if inspect.isclass(cls) and issubclass(cls, PlayerInteraction):
                player_types.append(cls.__name__)
        player_types_as_str = ', '.join(player_types)

        while True:
            name = input('How to call a player?\n')
            if name.isalpha():
                break
            print('Name must be a single word, alphabetic characters only')

        while True:
            try:
                kind = input(f'What kind of player is it ({player_types_as_str})?\n')
                kind = getattr(all_player_types, kind)
                break
            except AttributeError:
                print(f'Allowed player types are: {player_types_as_str}\n')
        return name, kind

def __main__():
    load_from_file = False
    if load_from_file:
        server = GameServer.load_game()
    else:
        server = GameServer.new_game(GameServer.get_players())
    server.save()
    server.run()

if __name__ == "__main__":
    __main__()



