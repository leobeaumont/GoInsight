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

if TYPE_CHECKING:
    from .game import Game
    from .move import Move

class Board:
    """
    Stores board's data.

    Args:
        game (Game): Game associated to the board.
        size (Tuple[int, int], optional): Size of the board (default to 19x19).
        moves (List[Move], optional): List of moves (if not provided, game moves are used).

    Attributes:
        game (Game): Game associated to the board.
        size (Tuple[int, int]): Size of the board.
        board (List[List[Optional[Move]]]): Representation of the board.
    """
    def __init__(
        self,
        game: "Game",
        size: Optional[Tuple[int, int]] = (19, 19),
        moves: Optional[List["Move"]] = None
    ):
        self.game = game
        self.size = size

        if moves is None:
            moves = self.game.moves
        self.board: List[List[Optional["Move"]]] = self.board_from_moves(moves)

    def board_from_moves(self, moves: List["Move"]) -> List[List[Optional["Move"]]]:
        """
        Create a board representation from a list of moves.

        Args:
            moves (List[Move]): List of moves.

        Returns:
            List[List[Optional[Move]]]: Representation of the board.

        Raises:
            ValueError: If the moves provided countain an illegal sequence.
        """
        board = [[None] * self.size[0] for _ in range(self.size[1])]

        for i, move in enumerate(moves):
            if not self.is_valid_pos(move.pos, board):
                raise ValueError(f"Board.board_from_moves(moves) -- Invalid position at index {i}: {move.pos}")
            
            x, y = move.pos
            board[y][x] = move

        return board        

    def is_valid_pos(self, pos: Tuple[int, int], board: Optional[List[List[Optional["Move"]]]] = None) -> bool:
        """
        Check if a position is valid on the board.

        Args:
            pos (Tuple[int, int]): Coordinates on board (first coord is left to right, second coord is top to bottom and both starts at 0).
            board (List[List[Optional[Move]]], optional): Board tested (default to object's board if not provided).

        Returns:
            bool: Wether the position is valid or not.
        """
        if board is None:
            board = self.board
            size = self.size
        else:
            size = (len(board[0]), len(board))

        x, y = pos
        x_size, y_size = size

        if x < 0 or y < 0:
            return False
        elif x >= x_size or y >= y_size:
            return False
        elif board[y][x] is not None:
            return False
        else:
            return True
    
    def area_selection_sub_board(self, corner1: Tuple[int, int], corner2: Tuple[int, int]) -> List[str]:
        """
        Extract area positions within a sub-board defined by the given corners.

        Args:
            corner1 (Tuple[int, int]): Coordinate of area's first corner.
            corner2 (Tuple[int, int]): Coordinate of area's second corner.

        Returns:
            List[str]: List of area positions within the sub-board.
        """

        x_c1, y_c1 = corner1
        x_c2, y_c2 = corner2

        x_min, x_max = sorted((x_c1, x_c2))
        y_min, y_max = sorted((y_c1, y_c2))


        area = []
        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max + 1):
                col = VALID_COLUMN_GTP[i]
                line = str(self.size[1] - j)
                area.append(col + line)
        
        return area
    
    def moves_sub_board(self, corner1: Tuple[int, int], corner2: Tuple[int, int]) -> dict:
        """
        Extract area that the next player can play within.

        Args:
            corner1 (Tuple[int, int]): Coordinate of area's first corner.
            corner2 (Tuple[int, int]): Coordinate of area's second corner.

        Returns:
            dict : List of moves within the sub-board.
        """
        
        player_to_move = self.game.next_color()

        area = self.area_selection_sub_board(corner1, corner2)
        
        return {player_to_move: area}


    def add_move(self, move: "Move"):
        """
        Add a move to the board.

        Args:
            move (Move): Move to add.

        Raises:
            ValueError: If the move is not valid.
        """
        if not self.is_valid_pos(move.pos):
            raise ValueError(f"Board.add_move(move) -- Invalid move: {move.pos}")
        
        x, y = move.pos
        self.board[y][x] = move

    def remove_move(self, move: "Move"):
        """
        Add a move to the board.

        Args:
            move (Move): Move to remove.

        Raises:
            ValueError: If the position of the move doesn't exist.
        """
        x, y = move.pos
        x_size, y_size = self.size

        if 0 <= x < x_size and 0 <= y < y_size:
            self.board[y][x] = None
        else:
            raise ValueError(f"Board.remove_board(move) -- Invalid position: {move.pos}")
