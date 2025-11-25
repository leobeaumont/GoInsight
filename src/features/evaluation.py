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
        Classify the move in one of the following categories.

            - BEST
            - EXCELLENT
            - GOOD
            - INACCURACY
            - MISTAKE
            - BLUNDER

        :param turn: Turn of the move classified.
        :type turn: int
        :return: Classification ("BEST"/"EXCELLENT"/...).
        :rtype: str
        :raises ValueError: If this is called before the analysis of the game.
        :raises ValueError: If the value of turn is invalid.
        """
        game_analysis = self.analizer.game_analysis
        if game_analysis is None:
            raise ValueError(f"Evaluator.classify_move(turn) -- Please run the game analysis before this method.")
        
        game_length = len(game_analysis)
        if turn >= game_length:
            raise ValueError(f"Evaluator.classify_move(turn) -- The value of turn is invalid for a game with {game_length} turns: {turn}")



    