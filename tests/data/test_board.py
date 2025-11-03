from typing import Optional, Tuple, TYPE_CHECKING, List
VALID_COLUMN_GTP = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
import pytest
from src.data import Game, Board, Move


def test_board_initialization():
    """
    Test the initialization of the Board class.
    """
    game = Game()
    board = Board(game)

    assert board.game == game
    assert board.size == (19, 19)
    assert board.sequence == []

def test_list_move_to_gtp():
    """
    Test the list_move_to_gtp method of the Board class.
    """
    game = Game()
    board = Board(game)

    move1 = Move("B", (3, 3))
    move2 = Move("W", "pass")
    board.sequence = [move1, move2]

    gtp_list = board.list_move_to_gtp()
    assert gtp_list == ["B D16"]  # Assuming (3,3) corresponds to D16 on a 19x19 board

def test_is_valid_pos():
    """
    Test the is_valid_pos method of the Board class.
    """
    game = Game()
    board = Board(game)

    valid_pos = (10, 10)
    invalid_pos = (20, 20)  # Assuming a 19x19 board

    assert board.is_valid_pos(valid_pos) == True
    assert board.is_valid_pos(invalid_pos) == False

def test_sub_board():
    """
    Test the sub_board method of the Board class.
    """
    game = Game()
    board = Board(game)

    corners = ("D4", "K10")
    # Validate corners before calling sub_board
    for corner in corners:
        assert corner[0] in VALID_COLUMN_GTP
        line = int(corner[1:])
        assert 1 <= line <= board.size[1]
    sub_board = board.sub_board(corners)

    assert isinstance(sub_board, Board)
    assert sub_board.size == (8, 7)  # Assuming D4 to K10 corresponds to an 8x7 board
    assert sub_board.game == game

@pytest.mark.parametrize("corners, expected_size", [
    (("A1", "C3"), (3, 3)),  # Valid range for a 19x19 board
    (("D4", "F6"), (3, 3)),  # Valid range for a 19x19 board
    (("J10", "L15"), (4, 6)),  # Adjusted to ensure "L15" is within valid range
])
def test_sub_board_sizes(corners, expected_size):
    """
    Test the sizes of sub-boards extracted using the sub_board method.
    """
    game = Game()
    board = Board(game)

    sub_board = board.sub_board(corners)
    assert sub_board.size == expected_size

