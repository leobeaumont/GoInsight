from copy import deepcopy
import json
import platform
import subprocess

from ..data import Game, SgfTree
from .constants import ANALYSIS_CONFIG_PATH, MODEL_DIR, NEURALNET_PATH

class Analizer:
    """
    Used to analyze different aspects of a game.
    """
    def __init__(self):
        pass

    @classmethod
    def katago_analysis(cls, tree: SgfTree):
        """
        This function performs an analysis of a Go game position using KataGo and returns the score lead and candidate moves.
        It creates an input file for KataGo, runs the analysis, reads the output file, and extracts the score lead from the results.

        Args:
            tree (SgfTree): The SGF tree representing the game position to analyze.

        Returns:
            float: The score lead at the current position.
            list: A list of candidate moves.
            float: The win probability at the current position.
        """
        # Katago selection depending on OS
        if platform.system() == "Darwin":
            model = "katago"
        elif platform.system() == "Linux":
            model = "/".join([MODEL_DIR, "katago"])
        else:
            model = "/".join([MODEL_DIR, "katago.exe"])

        # Obtaining data from SGF tree
        game = Game.from_sgftree(tree)
        moves_list = tree.move_sequence(insert_tuple=True)
        rules = game.ruleset
        komi = game.komi
        x, y = game.size
        initial_stones = [("B", sgf_pos) for sgf_pos in (game.AB or [])] + \
                         [("W", sgf_pos) for sgf_pos in (game.AW or [])]
        
        # Building input json
        json_input = {
            "id": "game_analysis",
            "moves": moves_list,
            "rules": rules,
            "komi": komi,
            "boardXSize": x,
            "boardYSize": y,
            "initialStones": initial_stones,
            "analyzeTurns": [turn for turn in range(0, len(moves_list))],
        }

        # Command declaration
        command = [
        model,
        "analysis",
        "-model", NEURALNET_PATH,
        "-config", ANALYSIS_CONFIG_PATH
        ]

        # Running the command
        process = subprocess.run(
            command,
            input=json.dumps(json_input) + "\n",
            capture_output=True,
            text=True,
            check=True,
        )

        # Capturing output
        output_lines = [line for line in process.stdout.splitlines() if line.strip()]
        output_data = [json.loads(line) for line in output_lines]

        return output_data

def without_last_move(tree: SgfTree):
    """
    Returns a new SgfTree without the last move.
    """
    new_tree = deepcopy(tree)
    current = new_tree
    parrent = None
    while len(current.children)>0:
        parrent = current
        current = current.children[0]
    if parrent is not None:
        parrent.children = []
    return new_tree

def rating_last_move(tree: SgfTree):
    """
    This function rates the last move played in a Go game position by comparing the score lead before and after the move using KataGo analysis.
    """
    score_lead_after = Analizer.katago_analysis(tree)[0]
    score_lead_before = Analizer.katago_analysis(without_last_move(tree))[0]
    rate = score_lead_after / score_lead_before * 100 #Percentage of precision compared to the best move
    return rate

def analyze_last_move(tree: SgfTree):
    """
    This function analyzes the last move played in a Go game position.
    """
    rate = rating_last_move(tree)
    penultimate_rate = rating_last_move(without_last_move(tree))

    if penultimate_rate < 10:
        if rate < 30:
            return "Missed opportunity"
    if rate <= 0 : 
        return "Blunder"
    if rate >= 99 : 
        return "Best move"
    if rate >= 60 :
        return "Good move"
    else : 
        return "Mistake"
    
def count_moves(tree: SgfTree):
    """
    This function counts the number of moves played in a Go game represented by an SgfTree.

    Args:
        tree (SgfTree): The SGF tree representing the game.

    Returns:
        int: The number of moves played in the game.
    """
    if tree is None:
        return 0
    count = 0
    current = tree
    while current.children:
        current = current.children[0]
        count += 1
    return count

def analyse_game(tree: SgfTree):
    """
    This function analyzes a Go game represented by an SgfTree and provides insights on the quality of moves played.

    Args:
        tree (SgfTree): The SGF tree representing the game.

    Returns:
        list[list]: A list of lists containing the score lead and winrate after each move of the game.
    """
    move_qualities = []
    current_tree = deepcopy(tree)
    total_moves = count_moves(tree)
    for _ in range(total_moves):
        scoreLead, _, winrate = Analizer.katago_analysis(current_tree)
        move_qualities.append([scoreLead, winrate])
        current_tree = without_last_move(current_tree)
    move_qualities.reverse()  # Reverse to match the original move order
    return move_qualities

if __name__ == "__main__":
    from src.data.sgf import SgfTree
    # Création de l'arbre racine
    test_game = SgfTree.from_sgf("games/sapindenoel.sgf")
    """test_game = SgfTree({"RU": ["japanese"], "KM": ["7.5"], "SZ": ["19"]})
    # On ajoute un coup noir puis blanc
    test_game.children.append(SgfTree({"B": ["dd"]}))
    test_game.children[0].children.append(SgfTree({"W": ["pp"]}))"""
    analysis = Analizer.katago_analysis(test_game)
    print(analysis)
    #move_qualities = analyse_game(test_game)
    #print("Move Qualities:", move_qualities)
"""    print("Score Lead:", score_lead)
    print("Candidate Moves:", candidate_moves)
    print("Win Rate:", winrate)"""