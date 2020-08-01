import random


class Player():

    def __init__(self):
        self.cards = []
        self.rank = ()
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
                self.remain_cards.append((suit, index + 1))

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
