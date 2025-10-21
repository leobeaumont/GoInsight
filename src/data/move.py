"""
move.py

This module handles Go moves creation, manipulation and export.

Modules:
    board -- handle manipulation and encoding of the board.
    game  -- handle manipulation and encoding of games.
    move  -- handle manipulation and encoding of moves.
    sgf   -- handle SGF parsing.
"""

from typing import Optional, Tuple, TYPE_CHECKING
from .constants import VALID_COLUMN_GTP, VALID_COLUMN_SGF

if TYPE_CHECKING:
    from .game import Game

class Move:
    """
    Stores move's data.

    Args:
        game (Game): Game associated to the move.
        color (str, optional): Color of the move (infered from the game if not provided or invalid).
        pos (Tuple[int, int], optional): Coordinates of the move on board (move is a 'pass' if not provided).

    Raises:
        ValueError: If the position provided is invalid.

    Attributes:
        game (Game): The game to play the move on.
        turn (int): Turn on which the move is played (starts at 0).
        color (str): Color playing the move ('b' for black and 'w' for white).
        pos (Tuple[int, int]): Coordinates on board (first coord is left to right, second coord is top to bottom and both starts at 0).

    Methods:
        to_gtp(): Export move to the gtp format.
    """

    def __init__(
        self,
        game: "Game",
        color: Optional[str] = None,
        pos: Optional[Tuple[int, int]] = None
    ):
        self.game = game
        
        if color in ['b', 'w']:
            self.color = color
        else:
            self.color = self.game.next_color()
        
        if pos is not None:
            if not self.game.is_valid_pos(pos):
                raise ValueError("Invalid position")
        self.pos = pos

    @classmethod
    def sgf_to_coord(cls, sgf_pos: str) -> Tuple[int, int]:
        """
        Translate sgf coordinate format to a simple coordinates.

        Args:
            sgf_pos (str): Coordinates in the SGF format.

        Return:
            (Tuple[int, int]): The corresponding coordinates.
        """
        return (VALID_COLUMN_SGF.index(sgf_pos[0]), VALID_COLUMN_SGF.index(sgf_pos[1]))

    def to_gtp(self) -> str:
        """
        Translate the move to the gtp format.
        
        Returns:
            (str): the move in gtp format.
        """
        out = self.color

        if self.pos is None:
            play = "pass"
        else:
            col = VALID_COLUMN_GTP[self.pos[0]]
            line = str(self.game.size[1] - self.pos[1])
            play = col + line
        
        out += " " + play
        
        return out
