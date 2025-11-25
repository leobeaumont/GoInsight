from typing import List

from .constants import MOVE_CLASSIFICATION_BOUNDS
from .analysis import Analizer

class Evaluator:
    """
    Used to classify the quality of plays.

    Args:
        analizer (Analizer): Analizer used to analyze the game.
    """
    def __init__(self, analizer: Analizer):
        self.analizer = analizer

    def classify_move(self, turn: int) -> str:
        """
        Docstring for classify_move
        
        :param self: Description
        :param turn: Description
        :type turn: int
        :return: Description
        :rtype: str
        """
    