"""
game.py

This module handles Go games import, manipulation and export.

Modules:
    board -- handle manipulation and encoding of the board.
    game  -- handle manipulation and encoding of games.
    move  -- handle manipulation and encoding of moves.
    sgf   -- handle SGF parsing.
"""

from typing import Optional, Tuple
from .move import Move
from .sgf import SgfTree

class Game:
    """
    Manages game's data with various tools.

    Args:
        RU (str): Ruleset (e.g.: Japanese). 
        SZ (str): Size of the board, non-square boards are supported. 
        KM (str): Komi. 
        HA (str, optional): Number of handicap stones given to Black. Placement of the handicap stones are set using the AB property. 
        AB (str, optional): Locations of Black stones to be placed on the board prior to the first move. 
        AW (str, optional): Locations of White stones to be placed on the board prior to the first move. 

    Attributes:
        attrname (attrtype): Attribut description.

    Methods:
        from_sgf(path): Create a Game object from an sgf file.
    """

    def __init__(
        self,
        RU: str,
        SZ: str,
        KM: str,
        HA: Optional[str] = "0",
        AB: Optional[str] = None,
        AW: Optional[str] = None,
        **kwargs
    ):
        self.rul
    
    @classmethod
    def from_sgftree(cls, tree: SgfTree) -> "Game":
        """
        Create a new Game object from an sgf tree.

        Args:
            tree (SgfTree): SgfTree of the game.
        
        Returns:
            (Game): The game provided in the sgf tree.
        """
        game = Game()

    def next_color() -> str:
        """
        Tells if it is black's or white's turn.

        Returns:
            (str): 'b' for black and 'w' for white.
        """
        # Notes: by default black start the game
        # If black has bonus stones to handicap white, white start the game. Except if black has only one bonus stone, then black starts the game.
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
