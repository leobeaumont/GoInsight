import json
import os
import platform
import subprocess
from ..data.sgf import SgfTree

def get_katago_score_mean(tree: SgfTree):
    """
    This function performs an analysis of a Go game position using KataGo and returns the score mean.
    It creates an input file for KataGo, runs the analysis, reads the output file, and extracts the score mean from the results.
    Args:
        tree (SgfTree): The SGF tree representing the game position to analyze.
    Returns:
        float: The score mean from the KataGo analysis.
    """
    if platform.system() == "Darwin":
        model_path="/opt/homebrew/share/katago/kata1-b18c384nbt-s9996604416-d4316597426.bin.gz"
    elif platform.system() == "Linux":
        model_path="/model/katago/kata1-b18c384nbt-s9996604416-d4316597426.bin.gz"
    else:
        model_path="C:\\katago\\kata1-b18c384nbt-s9996604416-d4316597426.bin.gz" #WINDOWS À CHANGER
        
    path_input = "../../games/analysis_input.txt"
    path_output = "../../analysis_output.json"
    moves_list = json.dumps(tree.to_gtp_move_list())

    json_text = f'{{"id":"pos1","moves":{moves_list},"rules":"japanese","komi":7.5,"boardXSize":19,"boardYSize":19,"maxVisits":100}}'

    with open(path_input, "w") as f:
        f.write(json_text + "\n")

    #We perform the analysis with Katago
    command = [
    "katago",
    "analysis",
    "-model", model_path,
    "-config", "../../analysis.cfg"
    ]

    with open(path_input, "r") as infile, open(path_output, "w") as outfile:
        subprocess.run(command, stdin=infile, stdout=outfile)

    if os.path.exists(path_input): #We delete the analysis_input.txt file
        os.remove(path_input)

    with open(path_output, "r") as f: #Read the analysis_output.json file
        txt = f.read()
    output_data = json.loads(txt) #We create a dictionary from the JSON text
    scoreMean = output_data["scoreMean"] 
    
    if os.path.exists(path_output):
        os.remove(path_output) #We delete the analysis_output.json file

    return scoreMean