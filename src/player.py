import json
import typing

from src.hand import Hand


class Player:
    def __init__(self, name: str, hand: Hand, score: int = 0, chips: int = 0):
        self.name = name
        self.hand = hand
        self.score = score
        self.chips = chips

    def __str__(self):
        return f'{self.name}({self.chips}): {self.hand}'

    def __eq__(self, other: typing.Self | str | dict):
        if isinstance(other, str):
            other = self.load(json.loads(other))
        if isinstance(other, dict):
            other = self.load(other)
        return self.name == other.name \
               and self.score == other.score \
               and self.hand == other.hand \
               and self.chips == other.chips

    def __hash__(self):
        return hash(self.name)

    def save(self) -> dict:
        return {
            'name': self.name,
            'hand': str(self.hand),
            'score': self.score,
            'chips': self.chips
        }

    @classmethod
    def load(cls, data: dict):
        return cls(name=data['name'], hand=Hand.load(data['hand']), score=int(data['score']), chips=int(data['chips']))
