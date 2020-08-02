import random
from collections import Counter
from heapq import nlargest
from typing import List, Tuple


class Player():

    def __init__(self):
        self.cards = []
        self.rank = {}
        self.rank_value = []


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
            self.determine_rank(player)

    def determine_rank(self, player: Player) -> None:
        all_cards = self.cards_on_board + player.cards
        self.is_flush(all_cards)

    def is_flush(self, all_cards: List[Tuple[str, int]]) -> List[int]:
        result = []
        calculate_dict = Counter([suit for suit, _ in all_cards])
        most_common = calculate_dict.most_common(1)
        if most_common[0][1] >= 5:
            result = [value for suit, value in all_cards if suit == most_common[0][0]]
            result = nlargest(5, result)
        return result


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
