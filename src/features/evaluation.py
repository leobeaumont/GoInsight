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
        Classify the move in one of the following categories:
            - BEST
            - EXCELLENT
            - GOOD
            - INACCURACY
            - MISTAKE
            - BLUNDER
        
        :param turn: Turn of the move classified
        :type turn: int
        :return: Classification ("BEST"/"EXCELLENT"/...)
        :rtype: str
        """
    