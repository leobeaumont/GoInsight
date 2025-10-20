"""
board.py

This module handles the Go board.

Modules:
    game -- handle manipulation and encoding of games.
    move -- handle manipulation and encoding of moves.
"""

from typing import *
if TYPE_CHECKING:
    from .game import Game 
from .move import Move

VALID_COLUMN = "ABCDEFGHJKLMNOPQRSTUVWXYZ"

from typing import List, Tuple, Optional, Set

class Board:
    """
    Represents the Go board state.

    Args:
        size (int): Size of the board.

    Attributes:
        size (int): Board width/height.
        grid (List[List[Optional[str]]]): 2D list storing 'b', 'w', or None for empty.
    """

    SIZE_DEFAULT = 19

    def __init__(self, size: int = SIZE_DEFAULT):
        """
        Create a board. By default size is 19 but you can choose between 4 and 19.
        """

        if size < 4 or size > 19:
            raise ValueError("Board size must be between 4 and 19")
        self.size = size
        self.grid: List[List[Optional[str]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]
    
    def is_on_board(self, pos: Tuple[int, int]) -> bool:
        """
        Check if the position given is valid.
        """

        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size

    def get(self, pos: Tuple[int, int]) -> Optional[str]:
        """
        Return the color at a given position.
        """

        x, y = pos
        if not self.is_on_board(pos):
            return None
        return self.grid[y][x]

    def play(self, pos: Tuple[int, int], color: Optional[str]):
        """
        Set a position to a color ('b', 'w', or None).
        """

        if not self.is_on_board(pos):
            raise ValueError("Position out of bounds")
        x, y = pos
        self.grid[y][x] = color

    def is_empty(self, pos: Tuple[int, int]) -> bool:
        """
        Check if a position is empty.
        """
        return self.get(pos) is None

    def clone(self) -> "Board":
        """
        Return the board.
        """
        return self.grid

    def __str__(self) -> str:
        """Return a human-readable representation of the board."""
        # Print top coordinate labels (A–T, skipping I)
        header = "   " + " ".join("ABCDEFGHJKLMNOPQRSTUVWXYZ"[:self.size])
        rows = []
        for i in range(self.size - 1, -1, -1):  # print from top (highest row) to bottom
            row_num = f"{i + 1:2}"
            # Replace None with '.' for empty points
            row_display = [stone if stone is not None else '.' for stone in self.grid[i]]
            row_str = " ".join(row_display)
            rows.append(f"{row_num} {row_str}")
        return header + "\n" + "\n".join(rows)
