from src.hand import Hand
from src.player import Player


def test_init():
    h = Hand.load('10 3 20')
    p = Player(name='Alex', hand=h, score=h.score(), chips=11)
    assert p.name == 'Alex'
    assert p.hand == h
    assert p.score == 33
    assert p.chips == 11

def test_str():
    h = Hand.load('10 3 20')
    p = Player(name='Alex', hand=h, score=h.score(), chips=11)
    assert str(p) == 'Alex(11): 10 3 20'

def test_save():
    h = Hand.load('10 3 20')
    p = Player(name='Alex', hand=h, score=h.score(), chips=11)
    assert p.save() == {'name': 'Alex', 'score': 33, 'chips': 11, 'hand': '10 3 20'}

def test_eq():
    h1 = Hand.load('10 3 20')
    h2 = Hand.load('10 3 20')
    p1 = Player(name='Alex', hand=h1, score=h1.score(), chips=11)
    p2 = Player(name='Alex', hand=h2, score=h2.score(), chips=11)
    assert p1 == p2

def test_load():
    data = {'name': 'Alex', 'score': 33, 'chips': 11, 'hand': '10 3 20'}
    h = Hand.load('10 3 20')
    p_expected = Player(name='Alex', hand=h, score=h.score(), chips=11)
    p = Player.load(data)
    assert p == p_expected