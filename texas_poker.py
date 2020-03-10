import random


class Game():

    def __init__(self):
        self.remain_cards = {}
        self.cards_on_board = {}
        self.card_faces = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.players = {}

    def shuffle_cards(self):
        for suit in ['spade', 'heart', 'diamond', 'club']:
            for index, face in enumerate(self.card_faces):
                self.remain_cards[suit + '_' + str(face)] = index + 1

    def distribute_a_random_card(self):
        for player in self.players.values():
            card = random.choice(list(self.remain_cards.keys()))
            player.cards[card] = self.remain_cards[card]
            del self.remain_cards[card]

    # Distribute a specific card to the player.
    def distribute_a_card(self, player, card):
        pass

    def distribute_a_random_card_on_board(self):
        card = random.choice(list(self.remain_cards.keys()))
        self.cards_on_board[card] = self.remain_cards[card]
        del self.remain_cards[card]

    def set_players(self, number_of_players):
        for number in range(number_of_players):
            self.players[f'Player_{number}'] = self.Player()

    def show_cards(self):
        for (key, value) in self.players.items():
            print(f'{key}: {value.cards}')
        print(f'Cards on board: {self.cards_on_board}')

    class Player():

        def __init__(self):
            self.cards = {}


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
