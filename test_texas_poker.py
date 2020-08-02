import pytest

from texas_poker import Game


def test_distribution():
    game = Game()
    game.shuffle_cards()
    game.set_players(3)
    game.distribute_a_random_card()
    game.distribute_a_random_card()
    game.distribute_a_random_card_on_board()
    game.distribute_a_random_card_on_board()
    game.distribute_a_random_card_on_board()
    game.distribute_a_random_card_on_board()
    game.distribute_a_random_card_on_board()
    assert(len(game.players) == 3)
    assert(len(game.players['Player_1'].cards) == 2)
    assert(len(game.cards_on_board) == 5)


def test_is_flush():
    game = Game()
    all_cards = [('diamond', 10), ('diamond', 9), ('diamond', 6), ('diamond', 8), ('club', 2), ('club', 7), ('heart', 9)]
    result = game.is_flush(all_cards)
    expected = []
    assert(result == expected)
    all_cards = [('diamond', 10), ('diamond', 9), ('diamond', 6), ('diamond', 8), ('diamond', 2), ('club', 7), ('heart', 9)]
    result = game.is_flush(all_cards)
    expected = [10, 9, 8, 6, 2]
    assert(result == expected)
    all_cards = [('diamond', 10), ('diamond', 9), ('diamond', 6), ('diamond', 8), ('diamond', 2), ('diamond', 14), ('heart', 9)]
    result = game.is_flush(all_cards)
    expected = [14, 10, 9, 8, 6]
    assert(result == expected)
