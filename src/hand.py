import typing

from src.card import Card


class Hand:
    def __init__(self, cards:  list[Card] = None):
        if cards is None:
            # может быть пустая рука
            cards = []
        self.cards: list[Card] = cards

    def __repr__(self):
        return self.save()

    def __eq__(self, other):
        if isinstance(other, str):
            other = Hand.load(other)
        return self.cards == other.cards

    def save(self) -> str:
        """Convert deck to string in 'b4 g7 y0' format."""
        scards = [c.save() for c in self.cards]         # ['b4', 'g7', 'y0']
        s = ' '.join(scards)
        return s

    @classmethod
    def load(cls, text: str) -> typing.Self:
        """Convert string in 'b4 g7 y0' format to Deck. Return deck."""
        cards = [Card.load(s) for s in text.split()]
        return cls(cards=cards)

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        self.cards.remove(card)

    def score(self):
        """Очки за карты"""
        arr = []
        for c in self.cards:
            arr.append(c.score())
        arr.sort()
        result = 0
        i = 0
        while i < len(arr):
            result += arr[i]
            i += 1
            while i < len(arr) and arr[i] == arr[i - 1] + 1:
                i += 1
        return result