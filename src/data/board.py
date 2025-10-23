"""
board.py

This module handles the board and its states.

Modules:
    board -- handle manipulation and encoding of the board.
    game  -- handle manipulation and encoding of games.
    move  -- handle manipulation and encoding of moves.
    sgf   -- handle SGF parsing.
"""

from typing import Optional, Tuple, TYPE_CHECKING, List
from .constants import VALID_COLUMN_GTP
import numpy as np

if TYPE_CHECKING:
    from .game import Game
    from .move import Move

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
        self.sequence = [Move]


    
    def move_to_gtp(self) -> List[str]:
        """
        Convert a list of Move objects to a list of moves in GTP format.

        Returns:
            List[str]: List in GTP format (e.g.: ["B D4", "W pass"]).
        """
        board = []
        for i in self.sequence:
            board.append(i.to_gtp())

        return board

    def is_valid_pos(self, pos: List[str]) -> bool:
        """
        Check if a position is valid on the board.

        Args:
            pos (Tuple[int, int]): Coordinates on board (first coord is left to right, second coord is top to bottom and both starts at 0).

        """
        columns = VALID_COLUMN_GTP[:self.size[0]]
        rows = [str(i+1) for i in range(self.size[1])]

        for coord in pos:
            if len(coord) < 4:
                return False
            if coord[0] not in ["W", "B"]:
                return False
            if coord[2:-1] != "pass":
                if coord[2] not in columns:
                    return False
                if coord[3:] not in rows:
                    return False
        return True
    
    def sub_board(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int]) -> np.ndarray:
        """
        Extract a sub-board from the current board.

        Args:
            top_left (Tuple[int, int]): Coordinates of the top-left corner of the sub-board.
            bottom_right (Tuple[int, int]): Coordinates of the bottom-right corner of the sub-board.
        """



                
            