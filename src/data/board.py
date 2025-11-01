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
        self.sequence: List[Move] = None


    
    def list_move_to_gtp(self) -> List[str]:
        """
        Convert a list of Move objects to a list of moves in GTP format.

        Returns:
            List[str]: List in GTP format (e.g.: ["B D4", "W pass"]).
        """
        board = []
        for i in self.sequence:
            if "pass" not in i.to_gtp:
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
    

    
    def sub_board(self, corners: Tuple[str, str]) -> "Board":
        """
        Extract a sub-board from the current board.

        Args:
            corners (Tuple[str, str]): Top-left and bottom-right corners in GTP format (e.g.: ("D4", "K10")).

        Returns:
            (Board): The sub-board.
        """

        rows = (min(VALID_COLUMN_GTP.index(corners[0][0]),VALID_COLUMN_GTP.index(corners[1][0])), max(VALID_COLUMN_GTP.index(corners[0][0]),VALID_COLUMN_GTP.index(corners[1][0])))
        cols = (min(int(corners[0][1:]),int(corners[1][1:])),max(int(corners[0][1:]),int(corners[1][1:])))


        new_size = (rows[1]-rows[0]+1, cols[1]-cols[0]+1)
        moves_to_keep = []

        moves_gtp = self.list_move_to_gtp()

        for i in moves_gtp:
            col = VALID_COLUMN_GTP.index(i[2])
            row = int(i[3:])

            if rows[0] <= col <= rows[1] and cols[0] <= row <= cols[1]:
                moves_to_keep.append(i)
        
        sub_board = Board(self.game, new_size, moves_to_keep)

        return sub_board

                
            