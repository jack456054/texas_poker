import random
from collections import Counter
from heapq import nlargest
from itertools import count, groupby
from typing import List, Tuple


class Player():

    def __init__(self):
        self.cards = []
        self.rank = None
        self.rank_values = []


class Game():

    def __init__(self):
        self.remain_cards = []
        self.cards_on_board = []
        self.players = {}
        self.all_ranks = {
            9: 'Straight flush',
            8: 'Four of a kind',
            7: 'Full house',
            6: 'Flush',
            5: 'Straight',
            4: 'Three of a kind',
            3: 'Two pairs',
            2: 'One pair',
            1: 'Nothing',
        }
        self.card_faces = {
            1: 'A',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: '10',
            11: 'J',
            12: 'Q',
            13: 'K',
            14: 'A',
        }

    def shuffle_cards(self) -> None:
        for suit in ['spade', 'heart', 'diamond', 'club']:
            for index in range(13):
                self.remain_cards.append((suit, index + 2))

    def distribute_a_card_to_players(self) -> None:
        for player in self.players.values():
            player.cards.append(self.distribute_a_card())

    def distribute_a_card(self, card: Tuple[str, int] = None) -> Tuple[str, int]:
        card = card if card else random.choice(self.remain_cards)
        if card not in self.remain_cards:
            raise Exception('Duplicate cards!')
        self.remain_cards.remove(card)
        return card

    def distribute_a_card_on_board(self, card: Tuple[str, int] = None) -> None:
        self.cards_on_board.append(self.distribute_a_card(card))

    def set_players(self, number_of_players: int) -> None:
        for number in range(number_of_players):
            self.players[f'Player_{number + 1}'] = Player()

    def card_face_mapping(self, cards: List[Tuple[str, int]]) -> List[Tuple[str, str]]:
        return [(suit, self.card_faces[value]) for suit, value in cards]

    def card_value_mapping(self, values: List[int]) -> List[str]:
        return [self.card_faces[value] for value in values]

    def show_cards(self) -> None:
        for (player_number, player) in self.players.items():
            print(f'{player_number}: {self.card_face_mapping(player.cards)}')
        print(f'Cards on board: {self.card_face_mapping(self.cards_on_board)}')

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

    def show_each_player_rank(self) -> None:
        for (player_number, player) in self.players.items():
            print(f'{player_number}: {self.all_ranks[player.rank]}, {self.card_value_mapping(player.rank_values)}')

    def determine_winner(self) -> None:
        winner_combination = max([(player.rank, player.rank_values) for _, player in self.players.items()])
        print('Winner(s):')
        for player_number, player in self.players.items():
            if (player.rank, player.rank_values) == winner_combination:
                print(f'* {player_number}')


if __name__ == "__main__":
    game = Game()
    game.shuffle_cards()
    game.set_players(3)
    game.distribute_a_card_to_players()
    game.distribute_a_card_to_players()
    # game.show_cards()
    game.distribute_a_card_on_board()
    game.distribute_a_card_on_board()
    game.distribute_a_card_on_board()
    # game.show_cards()
    game.distribute_a_card_on_board()
    # game.show_cards()
    game.distribute_a_card_on_board()
    game.show_cards()

    game.determine_each_player_rank()
    game.show_each_player_rank()
    game.determine_winner()
