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
