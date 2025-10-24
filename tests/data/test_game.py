import pytest
from src.data import Game


def test_next_color():
    """
    Tests the methods next_color.
    """
    game = Game(["japanese"], ["19"], ["6.5"])
    assert game.next_color() == "B"

    game.handicap = 2
    assert game.next_color() == "W"

    game.moves = ["W A19", "B A18"]
    assert game.next_color() == "W"

