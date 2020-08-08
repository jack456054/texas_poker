import random
from collections import Counter
from heapq import nlargest
from itertools import count, groupby
from typing import List, Tuple


class Player():

    def __init__(self):
        self.cards = []
        self.rank = {}
        self.rank_values = []


class Game():

    def __init__(self):
        self.remain_cards = []
        self.cards_on_board = []
        self.card_faces = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.players = {}
        self.all_ranks = {
            'straight_flush': 9,
            'four_of_a_kind': 8,
            'full_house': 7,
            'flush': 6,
            'straight': 5,
            'three_of_a_kind': 4,
            'two_pairs': 3,
            'one_pair': 2,
            'nothing': 1,
        }

    def shuffle_cards(self) -> None:
        for suit in ['spade', 'heart', 'diamond', 'club']:
            for index, face in enumerate(self.card_faces):
                self.remain_cards.append((suit, index + 2))

    def distribute_a_random_card(self) -> None:
        for player in self.players.values():
            card = random.choice(self.remain_cards)
            self.remain_cards.remove(card)
            player.cards.append(card)

    # Distribute a specific card to the player.
    def distribute_a_card(self, player, card):
        pass

    def distribute_a_random_card_on_board(self) -> None:
        card = random.choice(self.remain_cards)
        self.remain_cards.remove(card)
        self.cards_on_board.append(card)

    def set_players(self, number_of_players: int) -> None:
        for number in range(number_of_players):
            self.players[f'Player_{number}'] = Player()

    def show_cards(self) -> None:
        for (player_number, player) in self.players.items():
            print(f'{player_number}: {player.cards}')
        print(f'Cards on board: {self.cards_on_board}')

    def determine_each_player_rank(self) -> None:
        for (player_number, player) in self.players.items():
            all_cards = self.cards_on_board + player.cards
            player.rank, player.rank_values = self.determine_rank(all_cards)

    def determine_rank(self, all_cards: List[Tuple[str, int]]) -> Tuple[int, List[int]]:
        rank, rank_values = self.is_flush(all_cards)
        if rank:
            return (rank, rank_values)
        rank, rank_values = self.is_straight(all_cards)
        if rank:
            return (rank, rank_values)
        rank, rank_values = self.determine_duplicates(all_cards)
        if rank:
            return (rank, rank_values)

    def is_flush(self, all_cards: List[Tuple[str, int]]) -> Tuple[int, List[int]]:
        result = []
        calculate_dict = Counter([suit for suit, _ in all_cards])
        most_common = calculate_dict.most_common(1)
        if most_common[0][1] >= 5:

            # Straight flush:
            _, result = self.is_straight([(suit, value) for suit, value in all_cards if suit == most_common[0][0]])
            if result:
                return (9, result)

            result = [value for suit, value in all_cards if suit == most_common[0][0]]
            result = nlargest(5, result)
        return (6, result) if result else (0, result)

    def is_straight(self, all_cards: List[Tuple[str, int]]) -> Tuple[int, List[int]]:
        values = list(set(sorted([card for _, card in all_cards])))
        c = count()
        result = max((list(g) for _, g in groupby(values, lambda x: x - next(c))), key=len)
        if result == [2, 3, 4, 5] and 14 in values:
            result.insert(0, 1)
        return (0, []) if len(result) < 5 else (5, result[-1:-6:-1])

    def determine_duplicates(self, all_cards: List[Tuple[str, int]]) -> Tuple[int, List[int]]:
        values = sorted([value for _, value in all_cards])
        calculate_dict = Counter(values)
        most_common = calculate_dict.most_common()

        # Four of a kind.
        if most_common[0][1] == 4:
            values = list(filter(lambda x: x != most_common[0][0], values))
            return (8, [most_common[0][0]] * 4 + [values[-1]])

        # Full house or three of a kind.
        if most_common[0][1] == 3:
            if most_common[1][1] == 3:  # Full house.
                return (7, [max(most_common[0][0], most_common[1][0])] * 3 + [min(most_common[0][0], most_common[1][0])] * 2)
            if most_common[1][1] == 2:
                if most_common[2][1] == 2:
                    return (7, [most_common[0][0]] * 3 + [max(most_common[1][0], most_common[2][0])] * 2)
                else:
                    return (7, [most_common[0][0]] * 3 + [most_common[1][0]] * 2)
            else:  # Three of a kind.
                values = list(filter(lambda x: x != most_common[0][0], values))
                return (4, [most_common[0][0]] * 3 + values[-1:-3:-1])

        # Two pairs or one pair.
        if most_common[0][1] == 2:
            if most_common[1][1] == 2:  # Two pairs.
                if most_common[2][1] == 2:
                    pair_list = sorted([most_common[0][0], most_common[1][0], most_common[2][0]])
                    values = list(filter(lambda x: x != pair_list[-1] and x != pair_list[-2], values))
                else:
                    pair_list = sorted([most_common[0][0], most_common[1][0]])
                    values = list(filter(lambda x: x not in pair_list, values))
                return (3, [pair_list[-1]] * 2 + [pair_list[-2]] * 2 + [values[-1]])
            else:  # One pair.
                values = list(filter(lambda x: x != most_common[0][0], values))
                return (2, [most_common[0][0]] * 2 + values[-1:-4:-1])

        return (1, values[-1:-6:-1])  # Nothing.


if __name__ == "__main__":
    game = Game()
    game.shuffle_cards()
    game.set_players(3)
    game.distribute_a_random_card()
    game.distribute_a_random_card()
    game.show_cards()
    game.distribute_a_random_card_on_board()
    game.distribute_a_random_card_on_board()
    game.distribute_a_random_card_on_board()
    game.show_cards()
    game.distribute_a_random_card_on_board()
    game.show_cards()
    game.distribute_a_random_card_on_board()
    game.show_cards()

    game.determine_each_player_rank()
