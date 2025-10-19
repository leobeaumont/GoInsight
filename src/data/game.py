"""
game.py

This module handles Go games import, manipulation and export.

Modules:
    board -- handle manipulation and encoding of the board.
    game  -- handle manipulation and encoding of games.
    move  -- handle manipulation and encoding of moves.
    sgf   -- handle SGF parsing.
"""

from typing import Tuple
from .move import Move
from .sgf import SgfTree

class Game:
    """
    Manages game's data with various tools.

    Args:
        argname (argtype): Description of the arg. 

    Attributes:
        attrname (attrtype): Attribut description.

    Methods:
        from_sgf(path): Create a Game object from an sgf file.
    """

    def __init__(self):
        pass
    
    @classmethod
    def from_sgftree(cls, tree: SgfTree) -> "Game":
        """
        Create a new Game object from an sgf tree.

        Args:
            tree (SgfTree): SgfTree of the game.
        
        Returns:
            (Game): The game provided in the sgf tree.
        """
        return tree.to_game()

    def next_color() -> str:
        """
        Tells if it is black's or white's turn.

        Returns:
            (str): 'b' for black and 'w' for white.
        """
        # Notes: by default black start the game
        pass

    def is_valid_pos(pos: Tuple[int, int]) -> bool:
        """
        Tells if a position is valid for a move.

        Args:
            pos (Tuple[int, int]): Position to test.

        Returns:
            (bool): Wether the position is playable or not.
        """
        pass
