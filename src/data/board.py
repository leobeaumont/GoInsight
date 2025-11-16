"""
board.py

This module handles the board and its states.

Modules:
    board -- handle manipulation and encoding of the board.
    game  -- handle manipulation and encoding of games.
    move  -- handle manipulation and encoding of moves.
    sgf   -- handle SGF parsing.
"""

from typing import Set, Iterable, Optional, Tuple, TYPE_CHECKING, List
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
    
    def sub_board(self, corner1: Tuple[int, int], corner2: Tuple[int, int]) -> "Board":
        """
        Extract a sub-board from the current board.
        Coordinate format is (x, y) starting at 0 and both corners are included in the selection.

        Args:
            corner1 (Tuple[int, int]): Coordinate of area's first corner.
            corner2 (Tuple[int, int]): Coordinate of area's second corner.

        Returns:
            Board: The sub-board.
        """
        x_c1, y_c1 = corner1
        x_c2, y_c2 = corner2

        size = (abs(x_c1 - x_c2) + 1, abs(y_c1 - y_c2) + 1)
        moves = self.moves_sub_board(corner1, corner2)

        return Board(self.game, size, moves)
    
    def moves_sub_board(self, corner1: Tuple[int, int], corner2: Tuple[int, int]) -> List["Move"]:
        """
        Extract moves that are within a sub-board defined by the given corners.
        Coordinate format is (x, y) starting at 0 and both corners are included in the selection.

        Args:
            corner1 (Tuple[int, int]): Coordinate of area's first corner.
            corner2 (Tuple[int, int]): Coordinate of area's second corner.

        Returns:
            List[Move]: List of moves within the sub-board.
        """
        x_c1, y_c1 = corner1
        x_c2, y_c2 = corner2

        x_min, x_max = sorted((x_c1, x_c2))
        y_min, y_max = sorted((y_c1, y_c2))

        kept_moves = list()

        for move in self.game.moves:
            x, y = move.pos
            if x_min <= x <= x_max and y_min <= y <= y_max:
                kept_moves.append(move)

        return kept_moves

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
        

    def _neighbors(self, x: int, y: int) -> Iterable[Tuple[int, int]]:
        """
        Yield the orthogonal neighbors of a board coordinate.

        A neighbor is returned only if it lies within the board's boundaries.
        Neighbors follow 4-connectivity: left, right, up, down.

        Args:
            x (int): X-coordinate of the reference point (column).
            y (int): Y-coordinate of the reference point (row).

        Returns:
            Iterable[Tuple[int, int]]: An iterable yielding coordinates of all
            valid orthogonal neighbors.
        """
        x_size, y_size = self.size
        if x > 0: yield (x - 1, y)
        if x < x_size - 1: yield (x + 1, y)
        if y > 0: yield (x, y - 1)
        if y < y_size - 1: yield (x, y + 1)

    def _group_and_liberties(self, start: Tuple[int, int]) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]]]:
        """
        Compute the connected group of a stone and all its liberties.

        A group consists of all stones of the same color connected through
        orthogonal adjacency (4-neighborhood). Liberties are all empty
        intersections adjacent to any stone in the group.

        Args:
            start (Tuple[int, int]): Coordinate of the starting stone.

        Returns:
            Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]]]:
                - A set of coordinates representing the group.
                - A set of coordinates representing all liberties of that group.
        """
        x0, y0 = start
        stone = self.board[y0][x0]
        if stone is None:
            return set(), set()

        color = stone.color.lower()
        stack = [(x0, y0)]
        visited = set([(x0, y0)])
        group = set()
        liberties = set()

        while stack:
            x, y = stack.pop()
            group.add((x, y))
            for nx, ny in self._neighbors(x, y):
                cell = self.board[ny][nx]
                if cell is None:
                    liberties.add((nx, ny))
                elif cell.color.lower() == color and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append((nx, ny))

        return group, liberties

        
    def update_board(self) -> List[Tuple[int, int]]:
        """
        Detect and remove all captured groups from the board.

        A captured group is any set of stones with zero liberties.
        The function scans the entire board, evaluates each group once,
        removes the ones without liberties, and returns their coordinates.

        This function is rule-agnostic: it also removes self-captured stones.

        Returns:
            List[Tuple[int, int]]: Sorted list of coordinates of all stones
            removed during the capture resolution.
        """
        to_remove = set()
        visited = set()

        y_size = self.size[1]
        x_size = self.size[0]

        for y in range(y_size):
            for x in range(x_size):
                if self.board[y][x] is None:
                    continue
                if (x, y) in visited:
                    continue

                group, liberties = self._group_and_liberties((x, y))
                visited.update(group)

                if len(liberties) == 0:
                    to_remove.update(group)

        # Remove captured stones
        for x, y in to_remove:
            self.board[y][x] = None

        return [(x, y) for (x, y) in sorted(to_remove)]

