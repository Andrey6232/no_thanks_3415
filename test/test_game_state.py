from src.card import Card
from src.deck import Deck
from src.game_state import GameState
from src.player import Player

data = {
    'top': '7',
    'current_player_index': 1,
    'deck': '20 6 10',
    'players': [
        {
            'name': 'Alex',
            'hand': '3 6',
            'score': 5
        },
        {
            'name': 'Bob',
            'hand': '5',
            'score': 1
        },
        {
            'name': 'Charley',
            'hand': '7 10 20',
            'score': 3
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
    game1 = GameState(players=players, deck=full_deck, top=Card.load('7'))
    game2 = GameState(players=players.copy(), deck=full_deck, top=Card.load('7'))
    # надо бы еще game с отличающимися на 1 другой параметр и всеми отличающимися
    game3 = GameState(players=players, deck=Deck.load('20 6 10'), top=Card.load('7'))
    game4 = GameState(players=players, deck=Deck.load('20 6 10'), top=Card.load('8'))
    assert game1 == game2
    assert game1 != game3
    assert game3 != game4


def test_save():
    players = [alex, bob, charley]
    game = GameState(players=players, deck=Deck.load(data['deck']), top=Card.load(data['top']), current_player=1)
    assert game.save() == data


def test_load():
    game = GameState.load(data)
    assert game.save() == data


def test_next_player():
    game = GameState.load(data)
    assert game.current_player() == bob

    game.next_player()
    assert game.current_player() == charley

    game.next_player()
    assert game.current_player() == alex

    game.next_player()
    assert game.current_player() == bob


def test_draw_card():
    game = GameState.load(data)
    assert game.deck == '20 6 10'
    assert game.current_player().hand == '5'

    game.draw_card()
    assert game.deck == '20 6'
    assert game.current_player().hand == '5 10'


def test_play_card():
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=Card.load('7'), current_player=2)

    assert game.current_player().hand == '7 10 20'
    assert game.top == Card.load('7')

    game.play_card(Card.load('10'))
    assert game.current_player().hand == '7 20'
    assert game.top == Card.load('10')