"""
board.py

This module handles the board and its states.

Modules:
    board -- handle manipulation and encoding of the board.
    game  -- handle manipulation and encoding of games.
    move  -- handle manipulation and encoding of moves.
    sgf   -- handle SGF parsing.
"""

from typing import Optional, Tuple, TYPE_CHECKING
from .constants import VALID_COLUMN_GTP

if TYPE_CHECKING:
    from .game import Game

class Board:
    """
    Stores board's data.

    Args:
        game (Game): Game associated to the board.
        size (Tuple[int, int], optional): Size of the board (default to 19x19).

    Raises:
        ValueError: If the size of the board is invalid.

    Attributes:
        game (Game): Game associated to the board.
        size (Tuple[int, int]): Size of the board.

    Methods:
        TO DO
    """

    def __init__(
        self,
        game: "Game",
        size: Optional[Tuple[int, int]] = (19, 19)
    ):
        self.game = game
        self.size = size
