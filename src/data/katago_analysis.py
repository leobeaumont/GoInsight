"""
This is a Python program demonstrating how to run KataGo's
analysis engine as a subprocess and send it a query. 
It supports analyzing any sequence of moves provided via CLI.
"""

import argparse
import json
import subprocess
import time
from threading import Thread
import sgfmill
import sgfmill.boards
import sgfmill.ascii_boards
from typing import Tuple, List, Union, Literal, Any, Dict
import ast

Color = Union[Literal["b"], Literal["w"]]
Move = Union[None, Literal["pass"], Tuple[int, int]]

def sgfmill_to_str(move: Move) -> str:
    if move is None or move == "pass":
        return "pass"
    y, x = move
    return "ABCDEFGHJKLMNOPQRSTUVWXYZ"[x] + str(y + 1)

class KataGo:
    def __init__(self, katago_path: str, config_path: str, model_path: str, additional_args: List[str] = []):
        self.query_counter = 0
        self.katago = subprocess.Popen(
            [katago_path, "analysis", "-config", config_path, "-model", model_path, *additional_args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        def printforever():
            while self.katago.poll() is None:
                data = self.katago.stderr.readline()
                time.sleep(0)
                if data:
                    print("KataGo: ", data.decode(), end="")
            data = self.katago.stderr.read()
            if data:
                print("KataGo: ", data.decode(), end="")

        self.stderrthread = Thread(target=printforever)
        self.stderrthread.start()

    def close(self):
        self.katago.stdin.close()

    def query(self, initial_board: sgfmill.boards.Board, moves: List[Tuple[Color, Move]], komi: float, max_visits=None, sizeX: int = 19, sizeY: int = 19):
        query = {}
        query["id"] = str(self.query_counter)
        self.query_counter += 1

        query["moves"] = [(color, sgfmill_to_str(move)) for color, move in moves]
        query["initialStones"] = []

        for y in range(initial_board.side):
            for x in range(initial_board.side):
                color = initial_board.get(y, x)
                if color:
                    query["initialStones"].append((color, sgfmill_to_str((y, x))))

        query["rules"] = "Chinese"
        query["komi"] = komi
        query["boardXSize"] = sizeX
        query["boardYSize"] = sizeY
        query["includePolicy"] = True
        if max_visits is not None:
            query["maxVisits"] = max_visits

        return self.query_raw(query)

    def query_raw(self, query: Dict[str, Any]):
        self.katago.stdin.write((json.dumps(query) + "\n").encode())
        self.katago.stdin.flush()

        line = ""
        while line == "":
            if self.katago.poll():
                time.sleep(1)
                raise Exception("Unexpected katago exit")
            line = self.katago.stdout.readline().decode().strip()

        return json.loads(line)

def parse_moves(moves_input: str) -> List[Tuple[Color, Move]]:
    """
    Safely parse a Python list of moves, either passed as a Python object
    or as a string representation of a list.
    """
    try:
        moves = ast.literal_eval(moves_input)
    except Exception as e:
        raise ValueError(f"Could not parse moves list: {moves_input}\nError: {e}")

    # Validate format
    for item in moves:
        if not (isinstance(item, tuple) and len(item) == 2):
            raise ValueError(f"Invalid move format: {item}")
        color, move = item
        if color not in ('b', 'w'):
            raise ValueError(f"Invalid color: {color} in move {item}")
        if move != "pass" and not (isinstance(move, tuple) and len(move) == 2):
            raise ValueError(f"Invalid move position: {move} in move {item}")

    return moves

if __name__ == "__main__":
    description = "Example script showing how to run KataGo analysis engine and query it from Python."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-katago-path", required=True, help="Path to katago executable")
    parser.add_argument("-config-path", required=True, help="Path to KataGo analysis config")
    parser.add_argument("-model-path", required=True, help="Path to neural network .bin.gz file")
    parser.add_argument(
        "-moves-to-analyze",
        type=str,
        default="[]",
        help="Python list of moves, e.g. \"[('b',(3,0)),('w',(1,0))]"
    )
    parser.add_argument(
        "-sizeX-to-analyze",
        type=str,
        default="19",
        help="Size of the board"
    )
    parser.add_argument(
        "-sizeY-to-analyze",
        type=str,
        default="19",
        help="Size of the board"
    )

    args = vars(parser.parse_args())

    moves_to_analyze = parse_moves(args["moves_to_analyze"])
    print("Moves to analyze:", moves_to_analyze)

    katago = KataGo(args["katago_path"], args["config_path"], args["model_path"])

    sizeX = int(args["sizeX_to_analyze"])
    sizeY = int(args["sizeY_to_analyze"])

    board_size = max(sizeX,sizeY)  # Change if needed
    board = sgfmill.boards.Board(board_size)
    komi = 6.5

    # Apply moves to display board
    displayboard = board.copy()
    for color, move in moves_to_analyze:
        if move != "pass":
            y, x = move
            displayboard.play(y, x, color)

    print("Board position:")
    print(sgfmill.ascii_boards.render_board(displayboard))

    print("Query result:")
    print(katago.query(board, moves_to_analyze, komi, sizeX=sizeX, sizeY=sizeY))

    katago.close()
