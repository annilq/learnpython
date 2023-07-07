import collections

Card = collections.namedtuple("Card", ['rank', 'suit'])

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    value = rank_value * len(suit_values)+suit_values[card.suit]
    print(rank_value, value)
    return value


class FrenchDeck:
    ranks = [i for i in range(2, 11)]+list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self) -> None:
        self._cards = [Card(rank=rank, suit=suit)
                       for rank in self.ranks for suit in self.suits]
        self.index = 0

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, index):
        return self._cards[index]

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._cards):
            raise StopIteration
        value = self._cards[self.index]
        self.index += 1
        return value

bear_card = FrenchDeck()

for card in sorted(bear_card, key=spades_high):
    print(card)
