import random

from src.card import Card
from src.deck import Deck

cards = [Card(3), Card(10), Card(7)]

def test_init():
    d = Deck(cards=cards)
    assert d.cards == cards

def test_init_shuffle():
    """Проверяем, что карты в другом порядке."""
    full_deck1 = Deck(None)
    full_deck2 = Deck(None)
    assert full_deck1.cards != full_deck2.cards


def test_save():
    d = Deck(cards=cards)
    assert d.save() == '3 10 7'

    d = Deck(cards=[])
    assert d.save() == ''

def test_load():
    d = Deck.load('3 10 7')
    expected_deck = Deck(cards)
    # print()
    # print(type(d), d)
    # print(type(expected_deck), expected_deck)
    # так можно сравнивать, если нет метода __eq__
    assert str(d) == str(expected_deck)
    # так можно сравнивать, если есть метод __eq__
    assert d == expected_deck

def test_draw_card():
    d1 = Deck.load('3 10 7')
    d2 = Deck.load('3 10')
    c = d1.draw_card()
    assert c == Card.load('7')
    assert d1 == d2


def test_shuffle_1():
    cards = Card.all_cards(numbers=[5, 20, 9, 4, 11])
    deck = Deck(cards=cards)
    deck_list = [deck.save()]
    for i in range(5):
        deck.shuffle()
        s = deck.save()
        assert s not in deck_list
        deck_list.append(s)

def test_shuffle_2():
    random.seed(3)

    cards = Card.all_cards(numbers=[5, 20, 9, 4, 11])
    deck = Deck(cards=cards)
    deck_list = [deck.save()]

    deck.shuffle()
    assert deck.save() == '5 9 4 11 20'

    deck.shuffle()
    assert deck.save() == '9 11 4 5 20'

    deck.shuffle()
    assert deck.save() == '11 9 20 4 5'




