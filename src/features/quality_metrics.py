import json
import platform
import subprocess
from typing import List

from ..data import Game, SgfTree
from .constants import GAME_ANALYSIS_CONFIG_PATH, MODEL_DIR, NEURALNET_PATH, TURN_ANALYSIS_CONFIG_PATH

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
        turn_analysis (Dict[int, analysis]): Deep analysis of specific turn (dict key represent the turn). 

    Raises:
        ValueError: If player is not 'B' or 'W'.
    """
    def __init__(self, file: str, player: str = "B"):
        self.tree = SgfTree.from_sgf(file)

        if player != "B" and player != "W":
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

        # Sort by turn
        sorted_output_data = sorted(output_data, key=lambda x: x["turnNumber"])

        self.game_analysis = sorted_output_data

    def deep_turn_analysis(
            self,
            turn: int,
            selection: List[str] = None,
            invert_selection: bool = False
        ):
        """
        This function performs an analysis of a Go move in depth using KataGo.

        Args:
            turn (int): Turn fo the game to analize.
            selection (List[str], optional): List of positions in GTP format that KataGo must use (e.g.: ["C3","Q4","pass"]).
            invert_selection (bool): If true, the selection can't be used by KataGo (default to false).
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
            "analyzeTurns": [turn],
        }

        if selection:
            selected_moves = [{"player": moves_list[turn][0], "moves": selection, "untilDepth": turn + 10}]
            if invert_selection:
                json_input["avoidMoves"] = selected_moves
            else:
                json_input["allowMoves"] = selected_moves

        # Command declaration
        command = [
        model,
        "analysis",
        "-model", NEURALNET_PATH,
        "-config", TURN_ANALYSIS_CONFIG_PATH
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

        self.turn_analysis[turn] = output_data

    def game_score_lead(self) -> List[float]:
        """
        This function returns the score lead of black over the course of the game.

        Returns:
            List[float]: List of the score lead at every turn.

        Raises:
            ValueError: If the game analysis is not done yet.
        """
        if self.game_analysis is None:
            raise ValueError(f"Analizer.game_score_lead() -- Run the game analysis before this: Analizer.game_analysis = None")

        # Extract the score lead
        return [data["rootInfo"]["scoreLead"] for data in self.game_analysis]


if __name__ == "__main__":
    analizer = Analizer("games/sapindenoel_tronque.sgf")
    analizer.shalow_game_analysis()
    list_score_lead = analizer.game_score_lead()

    print("turn | scoreLead")
    for i, score_lead in enumerate(list_score_lead):
        if i < 10:
            print(f"{i}    | {score_lead}")
        elif i < 100:
            print(f"{i}   | {score_lead}")
        else:
            print(f"{i}  | {score_lead}")

    print(analizer.game_analysis[10])
