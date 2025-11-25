from typing import Dict, Tuple

MODEL_DIR = "model"

CONFIG_DIR = "configs"
ANALYSIS_CONFIG_PATH = "/".join([MODEL_DIR, "analysis_example.cfg"])
GAME_ANALYSIS_CONFIG_PATH = "/".join([CONFIG_DIR, "fast_game_analysis.cfg"])
TURN_ANALYSIS_CONFIG_PATH = "/".join([CONFIG_DIR, "deep_analysis.cfg"])

NEURALNET_DIR = "neuralnet"
NEURALNET_PATH = "/".join([NEURALNET_DIR, "g170e-b10c128-s1141046784-d204142634.bin.gz"])

# Lower and upper bounds of winrate loss for each move classification
MOVE_CLASSIFICATION_BOUNDS: Dict[str, Tuple[int, int]] = {
    "BEST": (-1.0, 0.0),
    "EXCELLENT": (0.0, 0.02),
    "GOOD": (0.02, 0.05),
    "INACCURACY": (0.05, 0.10),
    "MISTAKE": (0.10, 0.20),
    "BLUNDER": (0.20, 1.0)
    }
