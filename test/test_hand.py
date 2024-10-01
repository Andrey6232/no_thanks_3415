import random

from src.card import Card
from src.hand import Hand

cards = [Card(3), Card(10), Card(7)]

def test_init():
    d = Hand(cards=cards)
    assert d.cards == cards

def test_save():
    d = Hand(cards=cards)
    assert d.save() == '3 10 7'

    d = Hand(cards=[])
    assert d.save() == ''

def test_load():
    d = Hand.load('3 10 7')
    expected_deck = Hand(cards)
    # print()
    # print(type(d), d)
    # print(type(expected_deck), expected_deck)
    # так можно сравнивать, если нет метода __eq__
    assert str(d) == str(expected_deck)
    # так можно сравнивать, если есть метод __eq__
    assert d == expected_deck

def test_add_card():
    h = Hand.load('3 10 7')
    h.add_card(Card.load('20'))
    assert repr(h) == '3 10 7 20'

    h.add_card(Card.load('8'))
    assert repr(h) == '3 10 7 20 8'

def test_remove_card():
    h = Hand.load('3 10 7 20 8')
    c = Card.load('7')
    h.remove_card(c)
    assert repr(h) == '3 10 20 8'

def test_score():
    h = Hand.load('3 10 7')
    print(h.score())
    #assert h.score() == 10

    #h = Hand.load('20 9')
    #assert h.score() == 11