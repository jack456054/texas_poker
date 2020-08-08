from texas_poker import Game


def test_shuffle_cards():
    game = Game()
    game.shuffle_cards()
    assert(len(game.remain_cards) == 52)


def test_distribute_a_card_to_players():
    game = Game()
    game.set_players(3)
    game.shuffle_cards()
    game.distribute_a_card_to_players()
    assert(len(game.remain_cards) == 49)
    game.distribute_a_card_to_players()
    assert(len(game.remain_cards) == 46)


def test_distribute_a_card():
    game = Game()
    game.set_players(3)
    game.shuffle_cards()
    card = ('spade', 14)
    game.players['Player_1'].cards.append(game.distribute_a_card(card))
    assert(len(game.remain_cards) == 51)
    assert(card not in game.remain_cards)
    assert(card in game.players['Player_1'].cards)


def test_distribute_a_card_on_board():
    game = Game()
    game.set_players(3)
    game.shuffle_cards()
    game.distribute_a_card_on_board()
    assert(len(game.remain_cards) == 51)
    game.distribute_a_card_on_board()
    assert(len(game.remain_cards) == 50)


def test_set_players():
    game = Game()
    game.set_players(3)
    assert(len(game.players) == 3)


def test_distribution():
    game = Game()
    game.shuffle_cards()
    game.set_players(3)
    game.distribute_a_card_to_players()
    game.distribute_a_card_to_players()
    game.distribute_a_card_on_board()
    game.distribute_a_card_on_board()
    game.distribute_a_card_on_board()
    game.distribute_a_card_on_board()
    game.distribute_a_card_on_board()
    assert(len(game.players) == 3)
    assert(len(game.players['Player_1'].cards) == 2)
    assert(len(game.cards_on_board) == 5)


def test_is_flush():
    game = Game()
    all_cards = [('diamond', 10), ('diamond', 9), ('diamond', 6), ('diamond', 8), ('club', 2), ('club', 7), ('heart', 9)]
    result = game.is_flush(all_cards)
    expected = (0, [])
    assert(result == expected)
    all_cards = [('diamond', 10), ('diamond', 9), ('diamond', 6), ('diamond', 8), ('diamond', 2), ('club', 7), ('heart', 9)]
    result = game.is_flush(all_cards)
    expected = (6, [10, 9, 8, 6, 2])
    assert(result == expected)
    all_cards = [('diamond', 10), ('diamond', 9), ('diamond', 6), ('diamond', 8), ('diamond', 2), ('diamond', 14), ('heart', 9)]
    result = game.is_flush(all_cards)
    expected = (6, [14, 10, 9, 8, 6])
    assert(result == expected)

    # Straight flush.
    all_cards = [('diamond', 10), ('diamond', 9), ('diamond', 6), ('diamond', 8), ('diamond', 7), ('diamond', 14), ('heart', 9)]
    result = game.is_flush(all_cards)
    expected = (9, [10, 9, 8, 7, 6])
    assert(result == expected)


def test_is_straight():
    game = Game()
    all_cards = [('diamond', 10), ('diamond', 14), ('club', 6), ('diamond', 8), ('club', 2), ('club', 7), ('heart', 14)]
    result = game.is_straight(all_cards)
    expected = (0, [])
    assert(result == expected)
    all_cards = [('diamond', 10), ('diamond', 9), ('club', 6), ('diamond', 8), ('club', 2), ('club', 7), ('heart', 9)]
    result = game.is_straight(all_cards)
    expected = (5, [10, 9, 8, 7, 6])
    assert(result == expected)
    all_cards = [('diamond', 10), ('diamond', 9), ('club', 6), ('diamond', 8), ('diamond', 5), ('club', 7), ('heart', 9)]
    result = game.is_straight(all_cards)
    expected = (5, [10, 9, 8, 7, 6])
    assert(result == expected)
    all_cards = [('diamond', 10), ('diamond', 5), ('club', 4), ('diamond', 3), ('diamond', 2), ('diamond', 14), ('heart', 9)]
    result = game.is_straight(all_cards)
    expected = (5, [5, 4, 3, 2, 1])
    assert(result == expected)


def test_determine_duplicates():
    game = Game()

    # Four of a kind.
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 10), ('club', 2), ('club', 7), ('heart', 14)]
    result = game.determine_duplicates(all_cards)
    expected = (8, [10, 10, 10, 10, 14])
    assert(result == expected)
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 10), ('club', 2), ('club', 7), ('heart', 3)]
    result = game.determine_duplicates(all_cards)
    expected = (8, [10, 10, 10, 10, 7])
    assert(result == expected)

    # Full house.
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 2), ('club', 2), ('club', 7), ('heart', 14)]
    result = game.determine_duplicates(all_cards)
    expected = (7, [10, 10, 10, 2, 2])
    assert(result == expected)
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 2), ('club', 2), ('club', 7), ('heart', 7)]
    result = game.determine_duplicates(all_cards)
    expected = (7, [10, 10, 10, 7, 7])
    assert(result == expected)
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 2), ('club', 2), ('diamond', 2), ('heart', 7)]
    result = game.determine_duplicates(all_cards)
    expected = (7, [10, 10, 10, 2, 2])
    assert(result == expected)

    # Three of a kind.
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 2), ('club', 8), ('club', 7), ('heart', 14)]
    result = game.determine_duplicates(all_cards)
    expected = (4, [10, 10, 10, 14, 8])
    assert(result == expected)

    # Two pairs.
    all_cards = [('diamond', 10), ('spade', 10), ('club', 2), ('heart', 2), ('club', 8), ('club', 7), ('heart', 14)]
    result = game.determine_duplicates(all_cards)
    expected = (3, [10, 10, 2, 2, 14])
    assert(result == expected)
    all_cards = [('diamond', 10), ('spade', 10), ('club', 2), ('heart', 2), ('club', 14), ('club', 7), ('heart', 14)]
    result = game.determine_duplicates(all_cards)
    expected = (3, [14, 14, 10, 10, 7])
    assert(result == expected)
    all_cards = [('diamond', 10), ('spade', 10), ('club', 8), ('heart', 8), ('club', 14), ('club', 7), ('heart', 14)]
    result = game.determine_duplicates(all_cards)
    expected = (3, [14, 14, 10, 10, 8])
    assert(result == expected)

    # One pair.
    all_cards = [('diamond', 10), ('spade', 11), ('club', 2), ('heart', 2), ('club', 8), ('club', 7), ('heart', 14)]
    result = game.determine_duplicates(all_cards)
    expected = (2, [2, 2, 14, 11, 10])
    assert(result == expected)

    # Nothing.
    all_cards = [('diamond', 10), ('spade', 11), ('club', 3), ('heart', 2), ('club', 8), ('club', 7), ('heart', 14)]
    result = game.determine_duplicates(all_cards)
    expected = (1, [14, 11, 10, 8, 7])
    assert(result == expected)


def test_determine_rank():
    game = Game()

    # Flush.
    all_cards = [('diamond', 10), ('diamond', 9), ('diamond', 6), ('diamond', 8), ('diamond', 2), ('club', 7), ('heart', 9)]
    result = game.determine_rank(all_cards)
    expected = (6, [10, 9, 8, 6, 2])
    assert(result == expected)
    all_cards = [('diamond', 10), ('diamond', 9), ('diamond', 6), ('diamond', 8), ('diamond', 2), ('diamond', 14), ('heart', 9)]
    result = game.determine_rank(all_cards)
    expected = (6, [14, 10, 9, 8, 6])
    assert(result == expected)

    # Straight flush.
    all_cards = [('diamond', 10), ('diamond', 9), ('diamond', 6), ('diamond', 8), ('diamond', 7), ('diamond', 14), ('heart', 9)]
    result = game.determine_rank(all_cards)
    expected = (9, [10, 9, 8, 7, 6])
    assert(result == expected)

    # Straight.
    all_cards = [('diamond', 10), ('diamond', 9), ('club', 6), ('diamond', 8), ('club', 2), ('club', 7), ('heart', 9)]
    result = game.determine_rank(all_cards)
    expected = (5, [10, 9, 8, 7, 6])
    assert(result == expected)
    all_cards = [('diamond', 10), ('diamond', 9), ('club', 6), ('diamond', 8), ('diamond', 5), ('club', 7), ('heart', 9)]
    result = game.determine_rank(all_cards)
    expected = (5, [10, 9, 8, 7, 6])
    assert(result == expected)
    all_cards = [('diamond', 10), ('diamond', 5), ('club', 4), ('club', 3), ('diamond', 2), ('diamond', 14), ('heart', 9)]
    result = game.determine_rank(all_cards)
    expected = (5, [5, 4, 3, 2, 1])
    assert(result == expected)

    # Four of a kind.
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 10), ('club', 2), ('spade', 2), ('heart', 14)]
    result = game.determine_rank(all_cards)
    expected = (8, [10, 10, 10, 10, 14])
    assert(result == expected)
    game = Game()
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 10), ('club', 2), ('club', 7), ('heart', 3)]
    result = game.determine_rank(all_cards)
    expected = (8, [10, 10, 10, 10, 7])
    assert(result == expected)

    # Full house.
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 2), ('club', 2), ('club', 7), ('heart', 14)]
    result = game.determine_rank(all_cards)
    expected = (7, [10, 10, 10, 2, 2])
    assert(result == expected)
    game = Game()
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 2), ('club', 2), ('club', 7), ('heart', 7)]
    result = game.determine_rank(all_cards)
    expected = (7, [10, 10, 10, 7, 7])
    assert(result == expected)
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 2), ('club', 2), ('diamond', 2), ('heart', 7)]
    result = game.determine_rank(all_cards)
    expected = (7, [10, 10, 10, 2, 2])
    assert(result == expected)

    # Three of a kind.
    all_cards = [('diamond', 10), ('spade', 10), ('club', 10), ('heart', 2), ('club', 8), ('club', 7), ('heart', 14)]
    result = game.determine_rank(all_cards)
    expected = (4, [10, 10, 10, 14, 8])
    assert(result == expected)

    # Two pairs.
    all_cards = [('diamond', 10), ('spade', 10), ('club', 2), ('heart', 2), ('club', 8), ('club', 7), ('heart', 14)]
    result = game.determine_rank(all_cards)
    expected = (3, [10, 10, 2, 2, 14])
    assert(result == expected)
    all_cards = [('diamond', 10), ('spade', 10), ('club', 2), ('heart', 2), ('club', 14), ('club', 7), ('heart', 14)]
    result = game.determine_rank(all_cards)
    expected = (3, [14, 14, 10, 10, 7])
    assert(result == expected)
    all_cards = [('diamond', 10), ('spade', 10), ('club', 8), ('heart', 8), ('club', 14), ('club', 7), ('heart', 14)]
    result = game.determine_rank(all_cards)
    expected = (3, [14, 14, 10, 10, 8])
    assert(result == expected)

    # One pair.
    all_cards = [('diamond', 10), ('spade', 11), ('club', 2), ('heart', 2), ('club', 8), ('club', 7), ('heart', 14)]
    result = game.determine_rank(all_cards)
    expected = (2, [2, 2, 14, 11, 10])
    assert(result == expected)

    # Nothing.
    all_cards = [('diamond', 10), ('spade', 11), ('club', 3), ('heart', 2), ('club', 8), ('club', 7), ('heart', 14)]
    result = game.determine_rank(all_cards)
    expected = (1, [14, 11, 10, 8, 7])
    assert(result == expected)


def determine_winner(self):
    game.determine_each_player_rank()
