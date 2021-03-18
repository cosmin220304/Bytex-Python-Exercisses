import random


class Card:
    def __init__(self, color, number, sign):
        self._color = color
        self._number = number
        self._sign = sign

    def __str__(self):
        return f"{self._color} {self._number} {self._sign}"

    @property
    def color(self):
        return self._color

    @property
    def number(self):
        return self._number

    @property
    def sign(self):
        return self._sign


class Deck:
    cards_no = 52
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'K', 'Q', 'A']
    colors = ['blue', 'red']
    signs = ['hearts', 'spades', 'diamonds', 'clubs']

    def __init__(self):
        self._cards = [Card(color, number, sign) for number in self.numbers for color in self.colors for sign in self.signs]

    def shuffle(self):
        for _ in range(100000):
            i = random.randint(0, self.cards_no - 1)
            self._cards[i], self._cards[i+1] = self._cards[i+1], self._cards[i]

    def get_last_card(self):
        self.cards_no -= 1
        return self._cards.pop(0)

deck = Deck()
deck.shuffle()
card = deck.get_last_card()
print(card)
print(deck.cards_no)