"""
game.py

This module handles Go games import, manipulation and export.

Modules:
    board -- handle manipulation and encoding of the board.
    game  -- handle manipulation and encoding of games.
    move  -- handle manipulation and encoding of moves.
    sgf   -- handle SGF parsing.
"""

from typing import List, Optional, overload, Tuple, Union
from .board import Board
from .move import Move
from .sgf import SgfTree

class Game:
    """
    Manages game's data with various tools.

    Args:
        RU (List[str]): Ruleset (e.g.: Japanese). 
        SZ (List[str]): Size of the board, non-square boards are supported. 
        KM (List[str]): Komi. 
        HA (List[str], optional): Number of handicap stones given to Black. Placement of the handicap stones are set using the AB property. 
        AB (List[str], optional): Locations of Black stones to be placed on the board prior to the first move. 
        AW (List[str], optional): Locations of White stones to be placed on the board prior to the first move. 

    Attributes:
        ruleset (str): Ruleset (e.g.: Japanese).
        size (Tuple[int, int]): Width and height of the board, non-square boards are supported.
        komi (float): Komi.
        handicap (int): Number of handicap stones given to Black.
        board (Board): Board of the game, used to store board states.
        moves (List[str]): Sequence of moves in GTP format (e.g.: ["W A19", "B B18", "W pass"])
    """

    def __init__(
        self,
        RU: List[str],
        SZ: List[str],
        KM: List[str],
        HA: Optional[List[str]] = ["0"],
        AB: Optional[List[str]] = None,
        AW: Optional[List[str]] = None,
        **kwargs
    ):
        # Initialisation attributes
        self.ruleset: str = RU[0]
         
        size = [int(txt) for txt in SZ[0].split(":")]
        if len(size) == 1:
            size *= 2
        self.size: Tuple[int, int] = size

        self.komi: float = float(KM[0])

        self.handicap: int = int(HA[0])

        # Variable/storage attributes
        self.moves: List[Move] = list()
        self.board: Board = Board(self, size, self.moves)

        # Board setup
        if AB:
            self.place("black", [Move.sgf_to_coord(sgf_pos) for sgf_pos in AB])
        
        if AW:
            self.place("white", [Move.sgf_to_coord(sgf_pos) for sgf_pos in AW])
    
    @classmethod
    def from_sgftree(cls, tree: SgfTree) -> "Game":
        """
        Create a new Game object from an sgf tree.

        Args:
            tree (SgfTree): SgfTree of the game.
        
        Returns:
            (Game): The game provided in the sgf tree.
        """
        root_properties = tree.properties
        game = Game(**root_properties)

        game.moves.extend(tree.move_sequence())
        # A finir: il faut update le board avec la sequence de coups

    def next_color(self) -> str:
        """
        Tells if it is black's or white's turn.

        Returns:
            (str): 'B' for black and 'W' for white.
        """
        # Notes: by default black start the game
        # If black has bonus stones to handicap white, white start the game. Except if black has only one bonus stone, then black starts the game.
        if not self.moves:
            return "B" if self.handicap < 2 else "W"
        return "BW"[self.moves[-1][0] == "B"] # Returns 'W' if last move is 'B' and 'B' otherwise.

    def is_valid_pos(self, pos: Tuple[int, int]) -> bool:
        """
        Tells if a position is valid for a move.

        Args:
            pos (Tuple[int, int]): Position to test.

        Returns:
            (bool): Wether the position is playable or not.
        """
        return self.board.is_valid_pos(pos)
    
    @overload
    def place(self, color: str, pos: Tuple[int, int]): ...

    @overload
    def place(self, color: str, pos: List[Tuple[int, int]]): ...
    
    def place(self, color: str, pos: Union[Tuple[int, int], List[Tuple[int, int]]]):
        """
        Place one or more stones on the board without registering a move.

        Args:
            color (str): Color of the stone(s).
            pos (Tuple[int, int] | List[Tuple[int, int]]): Coordinates of the stone(s).

        Raises:
            ValueError: If the coordinates are invalid.
        """
        if isinstance(pos, tuple):
            #TODO
            pass
        elif isinstance(pos, list):
            #TODO
            pass
        else:
            raise ValueError(f"Game.place -- Invalid argument pos: {pos}")
        

    def play(self, move: str):
        """
        Play a move.

        Args:
            move (str): Move in the GTP format (e.g.: 'W A19').
        """
        # A finir quand on aura codé le Board !
        # penser a update la value de move.turn
        self.moves.append(move)
