"""Карты No_Thanks."""


class Card:
    NUMBERS = list(range(3, 36))

    def __init__(self, number: int):
        if number not in Card.NUMBERS:
            raise ValueError
        self.number = number

    def __repr__(self):
        # '3'
        return f'{self.number}'

    def __eq__(self, other):
        return self.number == other.number

    def save(self):
        return repr(self)

    @staticmethod
    def load(text: str):
        """From '4' to Card(4)."""
        return Card(number=int(text))

    @staticmethod
    def all_cards(numbers: None | list[int] = None):
        if numbers is None:
            numbers = Card.NUMBERS
        # cards = []
        #for num in numbers:
        #   cards.append(Card(number=num))
        cards = [Card(number=num) for num in numbers]
        return cards

