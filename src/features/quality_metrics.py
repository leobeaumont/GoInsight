from copy import deepcopy
import json
import platform
import subprocess

from ..data import Game, SgfTree
from .constants import GAME_ANALYSIS_CONFIG_PATH, MODEL_DIR, NEURALNET_PATH

class Analizer:
    """
    Used to analyze different aspects of a game.

    Args:
        file (str): Path to the SGF file of the game.
        player (str): Protagonist of the analysis ('B' or 'W').
    
    Attributes:
        tree (SgfTree): SGF tree of the game.
        player (str): Protagonist of the analysis ('B' or 'W').
        game_analysis: Shalow analysis of the full game.
        turn_analysis (Dict[int, Dict[str, Analysis]]): Deep analysis of specific turn (first key for the turn, second key for the board dimension). 

    Raises:
        ValueError: If player is not 'B' or 'W'.
    """
    def __init__(self, file: str, player: str = "B"):
        self.tree = SgfTree.from_sgf(file)

        if player != "B" or player != "W":
            raise ValueError(f"Analizer(file, player) -- The value of player must be 'B' or 'W' not: {player}")
        self.player = player

        self.game_analysis = None
        self.turn_analysis = dict()

    def shalow_game_analysis(self):
        """
        This function performs an analysis of a Go game using KataGo.
        """
        # Katago selection depending on OS
        if platform.system() == "Darwin":
            model = "katago"
        elif platform.system() == "Linux":
            model = "/".join([MODEL_DIR, "katago"])
        else:
            model = "/".join([MODEL_DIR, "katago.exe"])

        # Obtaining data from SGF tree
        game = Game.from_sgftree(self.tree)
        moves_list = self.tree.move_sequence(insert_tuple=True)
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
        "-config", GAME_ANALYSIS_CONFIG_PATH
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

        self.game_analysis = output_data


if __name__ == "__main__":
    from src.data.sgf import SgfTree
    # Création de l'arbre racine
    analizer = Analizer("games/sapindenoel.sgf")
    analizer.shalow_game_analysis()
    data = dict()
    for turn in analizer.game_analysis:
        data[turn["turnNumber"]] = (turn["rootInfo"]["scoreLead"], turn["rootInfo"]["winrate"])

    print("turn | scoreLead")
    for i in range(len(analizer.game_analysis)):
        if i < 10:
            print(f"{i}    | {data[i][0]}")
        elif i < 100:
            print(f"{i}   | {data[i][0]}")
        else:
            print(f"{i}  | {data[i][0]}")