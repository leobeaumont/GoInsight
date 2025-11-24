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
    Test the moves of sub-boards extracted using the moves_sub_board method.
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

def test_neighbors(x=10, y=10):
    """
    Test the _neighbors method of the Board class.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    board = Board(game)

    x, y = 10, 10
    neighbors = list(board._neighbors(x, y))

    expected_neighbors = [(9, 10), (11, 10), (10, 9), (10, 11)]

    assert set(neighbors) == set(expected_neighbors)


def test_group_liberties():
    """
    Test the group_liberties method of the Board class.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    board = Board(game)

    move = Move(game, "b", pos=(10, 10))
    board.add_move(move)
    move = Move(game, "b", pos=(10, 11))
    board.add_move(move)


    group = {(10, 10), (10, 11)}
    group_test, liberties_test = board.group_and_liberties((10, 10))

    print(liberties_test)
    print(group_test)

    assert group_test == group

    expected_liberties = {(9, 10), (11, 10), (10, 9), (10, 12), (9, 11), (11, 11)}

    assert liberties_test == expected_liberties

def test_update_board():
    """
    Test the update_board method of the Board class.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    board = Board(game)

    moves = [Move(game, "b", pos=(0, 0)),
             Move(game, "w", pos=(1, 0)),
             Move(game, "b", pos=(0, 1)),
             Move(game, "w", pos=(1, 1)),
             Move(game, "b", pos=(10, 10)),
             Move(game, "b", pos=(11, 11)),
             Move(game, "b", pos=(10, 12)),
             Move(game, "b", pos=(9, 11)),
             Move(game, "w", pos=(0, 2)),
             Move(game, "w", pos=(10, 11))]

    for i in moves:
        board.add_move(i)

    assert board.board[0][0] is None
    assert board.board[1][0] is None
    assert board.board[11][10] is None
