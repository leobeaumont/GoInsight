import pytest
from src.data import Game
from src.data import Move


def test_game_init_basic():
    """
    Test Game initialization with default arguments.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    
    assert game.ruleset == "Japanese"
    assert game.size == (19, 19)
    assert game.komi == 6.5
    assert game.handicap == 0
    assert len(game.moves) == 0
    assert game.board is not None


def test_game_init_with_AB_AW():
    """
    Test initialization with handicap stones and setup positions.
    """
    game = Game(
        RU=["Chinese"],
        SZ=["9"],
        KM=["5.5"],
        AB=["aa", "bb"],
        AW=["cc"],
    )

    # The board should contain these initial placements
    assert game.board is not None
    assert game.board.board[0][0].color == "B"
    assert game.board.board[1][1].color == "B"
    assert game.board.board[2][2].color == "W"

@pytest.mark.parametrize("size_input, expected", [
    (["19"], (19, 19)),
    (["9:13"], (9, 13)),
])
def test_game_init_size_parsing(size_input, expected):
    """
    Test parsing of SZ property into board size (supports rectangular boards).
    """
    game = Game(RU=["Japanese"], SZ=size_input, KM=["6.5"])
    assert game.size == expected


def test_next_color():
    """
    Tests the methods next_color.
    """
    game = Game(["japanese"], ["19"], ["6.5"])
    assert game.next_color() == "B"

    game.handicap = 2
    assert game.next_color() == "W"

    move = Move(game, "W", (0, 0))
    game.moves = [move]
    assert game.next_color() == "B"


def test_is_valid_pos():
    """
    Test validity check for positions on the board.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    assert game.is_valid_pos((0, 0))
    assert not game.is_valid_pos((-1, -1))
    assert not game.is_valid_pos((19, 19))  # outside board


def test_place_single_and_multiple():
    """
    Test placing single and multiple stones on the board.
    """
    game = Game(RU=["Japanese"], SZ=["9"], KM=["6.5"])
    game.place("B", (0, 0))
    game.place("W", [(1, 1), (2, 2)])
    assert game.board.board[0][0].color == "B"
    assert game.board.board[1][1].color == "W"
    assert game.board.board[2][2].color == "W"


def test_place_invalid_type():
    """
    Test that Game.place raises error with invalid argument types.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    with pytest.raises(ValueError):
        game.place("black", "invalid")


def test_play_adds_move():
    """
    Test playing a valid GTP move updates move list and board.
    """
    game = Game(RU=["Japanese"], SZ=["19"], KM=["6.5"])
    game.play("b A1")

    assert len(game.moves) == 1
    move = game.moves[0]
    assert move.color == "b"
    assert move.pos == (0, 18)
    assert move.turn == 0
    assert game.board is not None


def test_from_sgftree(tmp_path):
    """
    Integration test: creating a Game from an SGF tree.
    """
    # Build a minimal fake SGF tree object
    class DummyTree:
        def __init__(self):
            self.properties = {"RU": ["Japanese"], "SZ": ["19"], "KM": ["6.5"]}
        def move_sequence(self):
            return ["b A1", "w B2"]

    tree = DummyTree()
    game = Game.from_sgftree(tree)

    assert isinstance(game, Game)
    assert game.ruleset == "Japanese"
    assert game.size == (19, 19)
    assert game.komi == 6.5
    assert isinstance(game.moves[0], Move)
    assert game.moves[0].pos == (0, 18)
