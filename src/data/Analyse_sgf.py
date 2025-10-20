import subprocess
import shlex
from sgf_to_list import sgf_list
import ast


def run_katago_analysis(katago_path, config_path, model_path, moves_to_analyze, sizeX = "19", sizeY = "19"):
    """
    Executes the KataGo analysis command using subprocess.

    Args:
        katago_path (str): Path to the KataGo executable.
        config_path (str): Path to the KataGo configuration file.
        model_path (str): Path to the KataGo model file.
        moves_to_analyze (str): A string representation of the list of moves,
                                e.g., "[('b',(3,0)),('w',(1,0))]"
    """
    command = (
        f"python katago_analysis.py "
        f"-katago-path {shlex.quote(katago_path)} "
        f"-config-path {shlex.quote(config_path)} "
        f"-model-path {shlex.quote(model_path)} "
        f"-moves-to-analyze {shlex.quote(moves_to_analyze)} "
        f"-sizeX-to-analyze {shlex.quote(sizeX)} "
        f"-sizeY-to-analyze {shlex.quote(sizeY)}"
    )

    print(f"Executing command: {command}")

    try:
        # Use subprocess.run for a more modern and safer way to run external commands.
        # shell=True is used here because shlex.quote handles spaces in paths,
        # and we're building a single string command.
        # If your paths don't have spaces, you could use a list of arguments
        # with shell=False for slightly better security against injection,
        # but with shlex.quote, this approach is generally safe.
        result = subprocess.run(
            command,
            shell=True,
            check=True,  # Raise an exception for non-zero exit codes
            capture_output=True, # Capture stdout and stderr
            text=True # Decode stdout and stderr as text
        )

        print("\n--- KataGo Analysis Output ---")
        print(result.stdout)
        if result.stderr:
            print("\n--- KataGo Analysis Errors (if any) ---")
            print(result.stderr)
        print("\n--- Analysis Complete ---")

    except subprocess.CalledProcessError as e:
        print(f"\nError executing KataGo analysis: {e}")
        print(f"Command returned non-zero exit code {e.returncode}")
        print(f"Stdout:\n{e.stdout}")
        print(f"Stderr:\n{e.stderr}")
    except FileNotFoundError:
        print(f"\nError: The Python script 'analysis_katago.py' or KataGo executable '{katago_path}' was not found.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    # Define your paths and moves
    katago_exec_path = "/Users/marcelomiranda/Documents/IMT-L2/Commande_entreprise/KataGo/katago"
    config_file_path = "/Users/marcelomiranda/Documents/IMT-L2/Commande_entreprise/KataGo/my_benchmark.cfg"
    model_file_path = "/Users/marcelomiranda/Documents/IMT-L2/Commande_entreprise/KataGo/model.bin.gz"
    moves_string = "[('b', (1, 1)), ('w', (2, 1)), ('b', (2, 2)), ('w', (3, 2)), ('b', (2, 3)), ('w', (3, 3))]"


    game_name = input("Name of the game to analyze : ")
    path = f"/Users/marcelomiranda/Documents/IMT-L2/Commande_entreprise/KataGo/Matches/{game_name}.sgf"
    game = sgf_list(path)
    
    print("Choose coordonate and size to analyze e.g. A1")
    coord = input("Coord of new board : ")
    print("Size of the board to analyze (square or rectangular)")
    sizeX = input("SizeX to analyze : ")
    sizeY = input("SizeY to analyze : ")

    repere_X = (ord(coord[0])-ord('A'), ord(coord[0])-ord('A')+int(sizeX)-1)
    repere_Y = (int(coord[1])-1, int(coord[1]) + int(sizeY)-2)
    new_game =[]
    for i in game :
        if i[1][0]>=repere_X[0] and i[1][0]<=repere_X[1]:
            if i[1][1]>=repere_Y[0] and i[1][1]<=repere_Y[1]:
                new_pos = (i[0],(i[1][0]-repere_X[0],i[1][1]-repere_Y[0]))
                print(i)
                print(new_pos)
                new_game.append(new_pos)
    print(new_game)


    run_katago_analysis(
        katago_exec_path,
        config_file_path,
        model_file_path,
        str(new_game),
        sizeX,
        sizeY
    )