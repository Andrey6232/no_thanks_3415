import pytest

from src.card import Card


def test_init():
    c = Card(3)
    assert c.number == 3


def test_save():
    c = Card(3)
    assert repr(c) == '3'
    assert c.save() == '3'

    c = Card(7)
    assert repr(c) == '7'
    assert c.save() == '7'

def test_eq():
    c1 = Card(3)
    c2 = Card(3)
    c3 = Card(21)
    c4 = Card(11)
    c5 = Card(7)

    assert c1 == c2
    assert c1 != c3
    assert c1 != c4
    assert c1 != c5

def test_load():
    s = '3'
    c = Card.load(s)
    assert c == Card(3)

    s = '6'
    c = Card.load(s)
    assert c == Card(6)

def test_validation():
    with pytest.raises(ValueError):
        Card('h')
    with pytest.raises(ValueError):
        Card(1)
    with pytest.raises(ValueError):
        Card(0)
    with pytest.raises(ValueError):
        Card('3')

def test_all_cards():
    cards = Card.all_cards(numbers=[5, 21, 9])
    #print(cards)
    expected_cards = [
        Card.load('5'),
        Card.load('21'),
        Card.load('9')
    ]
    assert cards == expected_cards

    cards = Card.all_cards()
    assert len(cards) == 33