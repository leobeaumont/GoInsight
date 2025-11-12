import pytest
from src.data import Move

class FakeGame:
    def __init__(self, raise_error: bool):
        self.raise_error = raise_error
        self.size = (19, 19)

    def is_valid_pos(self, pos):
        return not self.raise_error
    
    def next_color(self):
        return 'b'

@pytest.mark.parametrize("kwargs",[
    dict(),
    {"color": 'b'},
    {"pos": (1, 1)},
    {"color": 'b', "pos": (1, 1)}
])
def test_move_constructor(kwargs):
    """
    Test the constructor of the Move class.
    """        
    game = FakeGame(False)
    move = Move(game, **kwargs)

    assert move.color in ['b', 'w']
    assert move.pos in [None, (1, 1)]

    game_with_error = FakeGame(True)
    error = False
    try:
        move = Move(game_with_error, pos=(1, 1))
    except ValueError:
        error = True
    assert error

@pytest.mark.parametrize("kwargs",[
    dict(),
    {"color": 'b'},
    {"pos": (1, 1)},
    {"color": 'b', "pos": (1, 1)}
])
def test_to_gtp(kwargs):
    """
    Test the to_gtp method.
    """
    game = FakeGame(False)
    move = Move(game, **kwargs)

    gtp_move = move.to_gtp()

    assert gtp_move[0] in ['b', 'w']
    assert gtp_move[1] == ' '
    assert gtp_move[2] in "ABCDEFGHJKLMNOPQRSTUVWXYZ" or gtp_move[2:] == "pass"
    assert gtp_move[3] in "123456789" or gtp_move[2:] == "pass"

@pytest.mark.parametrize("sgf_pos, expected_coord", [
    (
        "",
        None
    ),
    (
        "aa",
        (0, 0)
    ),
    (
        "ab",
        (0, 1)
    )
])
def test_sgf_to_coord(sgf_pos, expected_coord):
    """
    Tests the translation of an sgf position into coordinates.
    """
    assert Move.sgf_to_coord(sgf_pos) == expected_coord


@pytest.mark.parametrize("sgf_pos", [
    "  ",
    "!!",
    "A19"
])
def test_error_sgf_to_coord(sgf_pos):
    """
    Tests the failcases of sgf_to_coord.
    """
    error = False
    try:
        Move.sgf_to_coord(sgf_pos)
    except ValueError:
        error = True
    assert error


@pytest.mark.parametrize("sgf_pos, gtp_pos", [
    (
        "aa",
        "A19"
    ),
    (
        "tt",
        "U0"
    ),
    (
        "",
        "pass"
    )
])
def test_sgf_to_gtp(sgf_pos, gtp_pos):
    """
    tests the translation of an sgf position into a gtp position.
    """
    assert Move.sgf_to_gtp(sgf_pos, (19, 19)) == gtp_pos

@pytest.mark.parametrize("gtp_move, expected", [
    ("b A1", ("b", (0, 18))),
    ("w T19", ("w", (18, 0))),
    ("B D4", ("b", (3, 15))),
    ("W J10", ("w", (8, 9))),
    ("b pass", ("b", None))
])
def test_from_gtp_valid(gtp_move, expected):
    """
    Tests valid GTP moves parsing.
    """
    game = FakeGame(False)
    move = Move.from_gtp(game, gtp_move)

    assert move.color == expected[0]
    assert move.pos == expected[1]
    assert move.game == game


@pytest.mark.parametrize("gtp_move", [
    "b",                # Missing position
    "bA1",              # No space
    "b A1 extra",       # Too many arguments
    "x A1",             # Invalid color
    "w I1",             # Invalid column
    "b A0",             # Invalid row
    "b A20",            # Row out of range
    "",                 # Empty string
])
def test_from_gtp_invalid(gtp_move):
    """
    Tests invalid GTP moves that should raise ValueError.
    """
    game = FakeGame(False)
    with pytest.raises(ValueError):
        Move.from_gtp(game, gtp_move)
