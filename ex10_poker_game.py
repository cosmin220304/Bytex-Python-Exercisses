import random
from typing import List
from enum import Enum


class Card:
    def __init__(self, color, number, sign):
        self._color = color
        self._number = number
        self._sign = sign

    def __str__(self):
        return f'{self._number} {self._color} of {self._sign}'

    @property
    def color(self):
        return self._color

    @property
    def number(self):
        return self._number

    @property
    def sign(self):
        return self._sign


def print_cards(cards: List[Card]):
    for i in range(len(cards) - 1):
        print(cards[i], end=', ')
    print(cards[-1])


class Deck:
    cards_no = 52
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'K', 'Q', 'A']
    colors = ['black', 'red']
    signs = ['hearts', 'spades', 'diamonds', 'clubs']

    def __init__(self):
        self._cards = [Card(color, number, sign) for number in self.numbers for color in self.colors for sign in
                       self.signs]
        self.shuffle()

    def shuffle(self):
        for _ in range(100000):
            i = random.randint(0, self.cards_no - 1)
            self._cards[i], self._cards[i + 1] = self._cards[i + 1], self._cards[i]

    def get_last_card(self):
        self.cards_no -= 1
        return self._cards.pop(0)


class Decisions(Enum):
    CHECK = 0
    FOLD = 1
    BET = 2
    RAISE = 3


decisions = {
    Decisions.CHECK: 'check',
    Decisions.FOLD: 'fold',
    Decisions.BET: 'bet',
    Decisions.RAISE: 'raise'
}


class Player:
    def __init__(self, is_human: bool, idx: int):
        self._cards = []
        self._is_human = is_human
        self._money = 3000
        self._idx = idx

    @property
    def money(self):
        return self._money

    @property
    def cards(self):
        return self._cards

    def __str__(self):
        if self._is_human:
            return 'Human'
        else:
            return f'Computer {self._idx}'

    def give_card(self, card: Card):
        self._cards.append(card)

    def give_money(self, amount):
        self._money += amount

    def make_decision(self, can_check: bool, can_raise: bool, stake: int, drawn_cards: List[Card]):
        available_decisions = decisions.copy()
        if not can_check:
            del available_decisions[Decisions.CHECK]
        if self.money <= stake or not can_raise:
            del available_decisions[Decisions.RAISE]

        if not self._is_human:
            return random.choice(list(available_decisions))
        else:
            choice = -1
            while choice not in available_decisions:
                print('Make decision:')
                for key, value in available_decisions.items():
                    print(f'{key.value}: {value}')
                print('q: to see cards')
                print('w: to see stake')
                print('e: to see drawn cards')

                player_input = input('your choice: ')
                if player_input == 'q':
                    print_cards(self.cards)
                elif player_input == 'w':
                    print(stake)
                elif player_input == 'e':
                    print_cards(drawn_cards)
                else:
                    try:
                        choice = Decisions(int(player_input))
                    except:
                        print(f'Invalid input {player_input}')
            return choice

    def raise_amount(self, stake: int):
        if not self._is_human:
            raise_amount = random.randint(stake, self._money)
            self._money -= raise_amount
            return raise_amount
        else:
            raise_amount = 0
            while stake < raise_amount <= self._money:
                print(f'Choose raise between: {stake} and {self._money}')
                raise_amount = int(input())
            return raise_amount

    def bet_amount(self, stake: int):
        if stake >= self._money:
            money = self._money
            self._money = 0
            return money
        self._money -= stake
        return stake

    def discard_cards(self):
        self._cards = []


class Game:
    def __init__(self):
        self._players = []
        self._deck = Deck()
        self._drawn_cards = []
        self._small_blind = 5
        self._big_blind = 5
        self._current_stake = 0
        self._current_player_bets = dict()

    # @property
    # def players(self):
    #     return self._players
    #
    # @property
    # def drawn_cards(self):
    #     return self._drawn_cards
    #
    # @property
    # def small_blind(self):
    #     return self._small_blind
    #
    # @property
    # def big_blind(self):
    #     return self._big_blind
    #
    # @property
    # def current_player_bets(self):
    #     return self._current_player_bets

    def _init_players(self, players_no: int):
        for i in range(players_no):
            if i == 0:
                self._players.append(Player(is_human=True, idx=i))
                continue
            self._players.append(Player(is_human=False, idx=i))

    def start_game(self, players_no: int):
        self._init_players(players_no)
        self._start_round()

    def _start_round(self):
        self._small_blind, self._big_blind = self._big_blind, self._small_blind + self._big_blind
        self._current_player_bets = dict()
        for player in self._players:
            self._current_player_bets[player] = 0

        print(f'Small blind: {self._small_blind}, Big blind: {self._big_blind}')
        self._current_stake = self._big_blind
        self._give_cards_to_players()
        self._change_blind_turn()
        self._make_initial_bets()
        self._continue_round()

    def _continue_round(self):
        print('remaining players:')
        for player in self._current_player_bets:
            print(f'{str(player)} with {player.money}$')

        new_player_bets = dict()
        last_to_fold = None
        for player, bet in self._current_player_bets.items():
            print(f'{str(player)}\'s turn')
            can_check = (bet == self._current_stake)
            decision = player.make_decision(can_check=can_check, stake=self._current_stake,
                                            can_raise=True, drawn_cards=self._drawn_cards)
            print(f'{str(player)} {decisions[decision]}')

            if decision == Decisions.FOLD:
                last_to_fold = player
                player.discard_cards()
                continue

            elif decision == Decisions.CHECK:
                new_player_bets[player] = self._current_stake

            elif decision == Decisions.BET:
                player.bet_amount(self._current_stake)
                new_player_bets[player] = self._current_stake

            elif decision == Decisions.RAISE:
                self._current_stake = player.raise_amount(self._current_stake)
                print(f'New stake: {self._current_stake}')
                new_player_bets[player] = self._current_stake

        # Bet again if behind current stake (small blind still in game or raise happened)
        print('go again')
        remaining_player_bets = dict()
        for player, bet in new_player_bets.items():
            if bet != self._current_stake:
                print(f'{str(player)}\'s turn')
                decision = player.make_decision(can_check=False, stake=self._current_stake,
                                                can_raise=False, drawn_cards=self._drawn_cards)
                print(f'{str(player)} {decisions[decision]}')

                if decision == Decisions.FOLD:
                    last_to_fold = player
                    player.discard_cards()
                    continue

                elif decision == Decisions.BET:
                    player.bet_amount(self._current_stake)

            remaining_player_bets[player] = self._current_stake
        print('end of go again')

        self._current_player_bets = remaining_player_bets
        self._draw_cards()
        print_cards(self._drawn_cards)

        if len(self._current_player_bets.keys()) < 2 or len(self._drawn_cards) == 5:
            self._end_round(last_to_fold)
        else:
            self._continue_round()

    def _end_round(self, last_to_fold):
        print('End of round')

        print('Final cards:')
        print_cards(self._drawn_cards)

        print('Players\' cards:')
        for player in self._current_player_bets:
            print(player, end=': ')
            print_cards(player.cards)

        # Computing winner
        best_score = 0
        players_score_map = dict()
        winners: List[Player] = []
        for player in self._current_player_bets:
            score = compute_score(down_cards=self._drawn_cards, hand_cards=player.cards)
            players_score_map[player] = score
            best_score = max(score, best_score)
        for player, score in players_score_map.items():
            if score == best_score:
                winners.append(player)

        # If all players folded
        if len(winners) == 0:
            winners.append(last_to_fold)

        # Give money to winners
        won_money = int(sum(self._current_player_bets.values()) / len(winners))
        for winner in winners:
            winner.give_money(won_money)
            print(f'Player {str(winner)} won {won_money}$!\n')

        # Remove losers
        self._players = [player for player in self._players if player.money > 0]

        # Check if game has ended
        if len(self._players) == 1:
            print(f'Player {winners[0]} won!')
            return

        # Reset game state and start a new round
        for player in self._players:
            player.discard_cards()
        self._deck = Deck()
        self._drawn_cards = []
        self._start_round()

    def _give_cards_to_players(self):
        for _ in range(5):
            for player in self._players:
                _card = self._deck.get_last_card()
                player.give_card(_card)

    def _change_blind_turn(self):
        self._players = self._players[1:] + [self._players[0]]

    def _make_initial_bets(self):
        self._players[0].bet_amount(self._small_blind)
        self._current_player_bets[self._players[0]] = self._small_blind
        self._players[1].bet_amount(self._big_blind)
        self._current_player_bets[self._players[1]] = self._big_blind

    def _draw_cards(self):
        amount = 1
        if len(self._drawn_cards) == 0:
            amount = 3

        for _ in range(amount):
            _card = self._deck.get_last_card()
            self._drawn_cards.append(_card)


def compute_score(down_cards, hand_cards):
    # todo: make this actually compute real score
    return random.randint(0, 10)


game = Game()
game.start_game(4)
