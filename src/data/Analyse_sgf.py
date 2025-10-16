import subprocess
import shlex
from sgftolist import sgf_list
import ast


def run_katago_analysis(katago_path, config_path, model_path, moves_to_analyze, size_to_analyze):
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
        f"python analysis_katago.py "
        f"-katago-path {shlex.quote(katago_path)} "
        f"-config-path {shlex.quote(config_path)} "
        f"-model-path {shlex.quote(model_path)} "
        f"-moves-to-analyze {shlex.quote(moves_to_analyze)} "
        f"-size-to-analyze {shlex.quote(size_to_analyze)} "
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
    katago_exec_path = "/Users/.../katago"
    config_file_path = "/Users/.../my_benchmark.cfg"
    model_file_path = "/Users/.../model.bin.gz"

    path = "/Users/.../....sgf"
    game = sgf_list(path)
    
    print("Choose coordonate and size to analyze e.g. A1")
    coord = input("Coord of new board")
    size = input("Size to analyze")

    repere_X = (ord(coord[0])-ord('A'), ord(coord[0])-ord('A')+int(size)-1)
    repere_Y = (int(coord[1])-1, int(coord[1]) + int(size)-2)
    new_game =[]
    for i in game :
        if i[1][0]>=repere_X[0] and i[1][0]<=repere_X[1]:
            if i[1][1]>=repere_Y[0] and i[1][1]<=repere_Y[1]:
                new_game.append(i)


    run_katago_analysis(
        katago_exec_path,
        config_file_path,
        model_file_path,
        str(new_game),
        size
    )