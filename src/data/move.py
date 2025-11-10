"""
move.py

This module handles Go moves creation, manipulation and export.

Modules:
    board -- handle manipulation and encoding of the board.
    game  -- handle manipulation and encoding of games.
    move  -- handle manipulation and encoding of moves.
    sgf   -- handle SGF parsing.
"""

from typing import Dict, List, Optional, Tuple, TYPE_CHECKING
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
    """

    def __init__(
        self,
        game: "Game",
        color: Optional[str] = None,
        pos: Optional[Tuple[int, int]] = None
    ):
        self.game = game
        
        if color in ['B', 'W', 'b', 'w']:
            self.color = color
        else:
            self.color = self.game.next_color()
        
        if pos is not None:
            if not self.game.is_valid_pos(pos):
                raise ValueError("Invalid position")
        self.pos = pos
        self.turn = None

    @classmethod
    def sgf_to_coord(cls, sgf_pos: str) -> Optional[Tuple[int, int]]:
        """
        Translate SGF coordinate format to a simple coordinates.

        Args:
            sgf_pos (str): Coordinates in the SGF format.

        Returns:
            Tuple[int, int], optional: The corresponding coordinates.
        
        Raises:
            ValueError: If the sgf position has an invalid character.
        """
        if sgf_pos == "":
            return None
        return (VALID_COLUMN_SGF.index(sgf_pos[0]), VALID_COLUMN_SGF.index(sgf_pos[1]))
    
    @classmethod
    def sgf_to_gtp(cls, sgf_pos: str, board_size: Tuple[int, int]) -> str:
        """
        Translate SGF coordinate format to GTP coordinate format.

        Args:
            sgf_pos (str): Coordinates in the SGF format.

        Returns:
            str: The corresponding position in GTP format ('pass' if sgf_pos is empty).
        """
        coords = Move.sgf_to_coord(sgf_pos)

        if coords is None:
            return "pass"
        
        col = VALID_COLUMN_GTP[coords[0]]
        line = str(board_size[1] - coords[1])
        return col + line
    
    @classmethod
    def from_gtp(cls, game: "Game", gtp_move: str) -> "Move":
        """
        Create a move from a GTP instruction.

        Args:
            game (Game): Game to associate with the move.
            gtp_move (str): Move in the GTP format (e.g.: 'w A19').

        Returns:
            Move: Corresponding Move object.

        Raises:
            ValueError: If the instruction is not under GTP format.
        """
        parsed = gtp_move.split(" ")

        if len(parsed) != 2:
            raise ValueError(f"Move.from_gtp(gtp_move) -- Invalid argument gtp_move: {gtp_move}")
        
        color, gtp_pos = parsed

        if color.lower() not in ["b", "w"]:
            raise ValueError(f"Move.from_gtp(gtp_move) -- Invalid argument gtp_move: {gtp_move}")
        
        if gtp_pos == "pass":
            pos = None
        else:
            x = VALID_COLUMN_GTP.index(gtp_pos[0].upper())
            y = game.size[1] - int(gtp_pos[1:])
            if not 0 <= y <= game.size[0] - 1:
                raise ValueError(f"Move.from_gtp(gtp_move) -- Invalid argument gtp_move: {gtp_move}")
            pos = (x, y)

        return Move(game, color.lower(), pos)
            
    def to_gtp(self) -> str:
        """
        Translate the move to the GTP format.
        
        Returns:
            str: the move in GTP format.
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
    
    def to_sgf(self) -> Dict[str, List[str]]:
        """
        Translate the move to the SGF format.

        Returns:
            Dict[str,List[str]]: Key encode the color and value is the position in SGF format inserted in a list. 
        """
        x, y = self.pos
        pos_sgf = VALID_COLUMN_SGF[x] + VALID_COLUMN_SGF[y]

        return {self.color.upper(): [pos_sgf]}

