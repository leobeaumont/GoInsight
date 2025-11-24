from typing import Optional, Tuple, TYPE_CHECKING, List
VALID_COLUMN_GTP = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
import pytest
from src.data import Game, Board, Move


def test_board_initialization():
    """
    Test the initialization of the Board class.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    board = Board(game)

    assert board.game == game
    assert board.size == (19, 19)
    for i in range(19):
        for j in range(19):
            assert board.board[i][j] is None
 
def test_is_valid_pos():
    """
    Test the is_valid_pos method of the Board class.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    board = Board(game)
    move = Move(game, pos=(10, 10))

    valid_pos = (10, 10)
    invalid_pos = (20, 20)  # Assuming a 19x19 board

    assert board.is_valid_pos(valid_pos) == True
    assert board.is_valid_pos(invalid_pos) == False

    board.add_move(move)

    assert board.is_valid_pos(valid_pos) == False # Position already played   

def test_area_selection_positions():
    """
    Test the moves of sub-boards extracted using the moves_sub_board method.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    board = Board(game)

    corner1 = (1, 1)
    corner2 = (2, 2)

    area_positions = board.area_selection_positions(corner1, corner2)

    assert len(area_positions) == 4
    assert "B18" in area_positions
    assert "B17" in area_positions
    assert "C18" in area_positions
    assert "C17" in area_positions

def test_add_remove_move():
    """
    Test the add_move and remove_move methods.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    board = Board(game)
    move = Move(game, pos=(10, 10))

    assert board.board[10][10] is None

    board.add_move(move)

    assert board.board[10][10] is not None

    board.remove_move(move)

    assert board.board[10][10] is None
