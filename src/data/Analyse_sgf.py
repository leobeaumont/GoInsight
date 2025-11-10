import subprocess
import shlex
from sgf_to_list import sgf_list



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
        f"python src/data/katago_analysis.py "
        f"-katago-path ./model/katago "
        f"-config-path ./model/default_gtp.cfg "
        f"-model-path ./neuralnet/kata1-b28c512nbt-adam-s11165M-d5387M.bin.gz "
        f"-moves-to-analyze {shlex.quote(moves_to_analyze)} "
        f"-sizeX-to-analyze {shlex.quote(sizeX)} "
        f"-sizeY-to-analyze {shlex.quote(sizeY)}"
    )

    print(f"Executing command: {command}")

    try:
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

    return result.stdout