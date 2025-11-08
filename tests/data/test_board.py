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

def test_sub_board():
    """
    Test the sub_board method of the Board class.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    board = Board(game)

    corner1 = (0, 0)
    corner2 = (7, 6)
    sub_board = board.sub_board(corner1, corner2)

    assert isinstance(sub_board, Board)
    assert sub_board.size == (8, 7)
    assert sub_board.game == game

def test_moves_sub_board():
    """
    Test the sizes of sub-boards extracted using the sub_board method.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    moves = [Move(game, pos=(0, 0)),
             Move(game, pos=(10, 10)),
             Move(game, pos=(1, 1)),
             Move(game, pos=(10, 9))]
    game.moves = moves
    board = Board(game)

    corner1 = (0, 0)
    corner2 = (9, 9)

    moves_sub_board = board.moves_sub_board(corner1, corner2)

    assert len(moves_sub_board) == 2
    assert moves_sub_board[0] == moves[0]
    assert moves_sub_board[1] == moves[2]
