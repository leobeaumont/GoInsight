"""
Handles all actions related to the stones on the board.
"""

from typing import List, Tuple, Set
from .board import Board


class StoneLogic:
    """
    Handles stone-related operations for a Go board.

        Args:
        board (Board): Stage of a game represented by its board.
    """

    def __init__(self, board: Board):

        self.board = board


    def neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Return on-board neighboring coordinates.
        """
        x, y = pos
        potential = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return [p for p in potential if self.board.is_on_board(p)]

    def group_at(self, pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """
        Find the entire connected group at position.
        """
        color = self.board.get(pos)
        if color is None:
            return set()
        group = set()
        to_visit = [pos]
        while to_visit:
            p = to_visit.pop()
            if p not in group:
                group.add(p)
                for n in self.neighbors(p):
                    if self.board.get(n) == color:
                        to_visit.append(n)
        return group

    def liberties(self, group: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """
        Get all liberties for a given group.
        """
        libs = set()
        for pos in group:
            for n in self.neighbors(pos):
                if self.board.get(n) is None:
                    libs.add(n)
        return libs

    def remove_group(self, group: Set[Tuple[int, int]]):
        """Remove all stones in a group."""
        for pos in group:
            self.board.set(pos, None)

    def place_stone(self, color: str, pos: Tuple[int, int]):
        """
        Place a stone and handle captures and legality.
        Raises ValueError if illegal (occupied, suicide).
        """
        if not self.board.is_on_board(pos):
            raise ValueError("Move out of bounds")
        if not self.board.is_empty(pos):
            raise ValueError("Position already occupied")

        if color == 'w':
            opponent = 'b'
        else :
            opponent = 'w'
        self.board.play(pos, color)
        captured_any = False

        # Check captures
        for n in self.neighbors(pos):
            if self.board.get(n) == opponent:
                group = self.group_at(n)
                if not self.liberties(group):
                    self.remove_group(group)
                    captured_any = True

        # Check for suicide
        group = self.group_at(pos)
        if not self.liberties(group) and not captured_any:
            self.board.set(pos, None)
            raise ValueError("Illegal move: suicide")
