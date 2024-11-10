from src.card import Card
from src.deck import Deck
from src.game_state import GameState
from src.hand import Hand
from src.player import Player

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

alex = Player.load(data['players'][0])
bob = Player.load(data['players'][1])
charley = Player.load(data['players'][2])
full_deck = Deck(None)


def test_init():
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, current_player=1, top=Card.load('7'))
    assert game.players == players
    assert game.deck == full_deck
    assert game._current_player == 1
    assert str(game.top) == '7'


def test_current_player():
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=Card.load('7'))
    assert game.current_player() == alex

    game = GameState(players=players, deck=full_deck, top=Card.load('7'), current_player=1)
    assert game.current_player() == bob

    game = GameState(players=players, deck=full_deck, top=Card.load('7'), current_player=2)
    assert game.current_player() == charley


def test_eq():
    players = [alex, bob, charley]
    game1 = GameState(players=players, deck=full_deck, top=Card.load('7'), chips=5)
    game2 = GameState(players=players.copy(), deck=full_deck, top=Card.load('7'), chips=5)
    game3 = GameState(players=players, deck=Deck.load('20 6 10'), top=Card.load('7'), chips=7)
    game4 = GameState(players=players, deck=Deck.load('20 6 10'), top=Card.load('8'), chips=7)
    game5 = GameState(players=players, deck=Deck.load('20 6 10'), top=Card.load('8'), chips=9)
    assert game1 == game2
    assert game1 != game3
    assert game3 != game4
    assert game4 != game5


def test_save():
    players = [alex, bob, charley]
    game = GameState(players=players, deck=Deck.load(data['deck']), top=Card.load(data['top']), current_player=0, chips=12)
    assert game.save() == data


def test_load():
    game = GameState.load(data)
    assert game.save() == data


def test_next_player():
    game = GameState.load(data)
    assert game.current_player() == alex

    game.next_player()
    assert game.current_player() == bob

    game.next_player()
    assert game.current_player() == charley

    game.next_player()
    assert game.current_player() == alex


def test_draw_card():
    game = GameState.load(data)
    assert game.deck == '20 6 10'
    assert game.current_player().hand == '3 8'
    game.draw_card()
    assert game.deck == '20 6'
    assert game.current_player().hand == '3 8 10'


def test_take_card():
    game = GameState.load(data)
    chips = game.current_player().chips
    game.take_card()
    assert game.current_player().hand == Hand.load('3 8 7')
    assert game.current_player().chips == game.chips + chips

    game.next_player()
    chips = game.current_player().chips
    game.take_card()
    assert game.current_player().hand == Hand.load('5 7')
    assert game.current_player().chips == game.chips + chips


def test_to_pay():
    game = GameState.load(data)
    assert game.current_player().chips == 7
    assert game.chips == 12
    game.to_pay()
    assert game.current_player().chips == 1
    assert game.chips == 13
    game.to_pay()
    assert game.current_player().chips == 4
    assert game.chips == 14
    game.to_pay()
    assert game.current_player().chips == 6
    assert game.chips == 15


def test_score_players():
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=Card.load('7'), current_player=0, chips=4)
    assert game.score_players() == {'Alex': 4, 'Bob': 4, 'Charley': 37}