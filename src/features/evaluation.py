"""
Module for evaluating move quality and the state of the game.

Functions:
- get_move_quality: Assigns a quality "stamp" (e.g., "Brilliant", "Blunder")
                    to a move by comparing it to the engine's best options.
- get_game_phase: Determines the game phase (Opening, Middlegame, Endgame)
                  based on the move number.
"""

# --- Constants for Quality Stamps (based on Winrate Loss) ---

# A "Brilliant" move is the best move AND it's significantly better
# than the second-best option (it was the only "true" good move).
BRILLIANT_WINRATE_GAP = 0.15  # 15% more winrate than the 2nd best move

# A "Best Move" is not necessarily the #1 move, but it's very close.
BEST_MOVE_THRESHOLD = 0.02  # Max 2% winrate loss compared to the best

# A "Good Move" is a solid move that doesn't lose much.
GOOD_MOVE_THRESHOLD = 0.05  # Max 5% winrate loss

# An "Inaccuracy" is a move that is not optimal.
INACCURACY_THRESHOLD = 0.10 # Max 10% winrate loss

# An "Error" starts to be a serious problem.
ERROR_THRESHOLD = 0.20      # Max 20% winrate loss

# Anything above 20% loss is a "Blunder".


# --- Constants for Game Phases (based on a 19x19 board) ---
# These values are approximate and can be adjusted.
OPENING_MOVES_END = 40
MIDGAME_MOVES_END = 180


def get_move_quality(user_move_analysis: dict, engine_top_moves: list[dict]) -> dict:
    """
    Assigns a quality "stamp" to a move by comparing it to the
    engine's best options.

    Args:
        user_move_analysis (dict): The engine's analysis object for the
                                   specific move the user played.
                                   Must contain at least 'winrate' and 'move'.
                                   Ex: {'move': 'D4', 'winrate': 0.45, ...}
        
        engine_top_moves (list[dict]): List of the engine's top moves,
                                       sorted from best to worst, for this position.
                                       Must contain at least the best move.
                                       Ex: [{'move': 'C4', 'winrate': 0.65, ...}, ...]

    Returns:
        dict: A dictionary containing a 'label' (e.g., "Error") and
              a 'description' (e.g., "This move loses 15% winrate.").
    """
    
    # Error case: if the engine provided no moves
    if not engine_top_moves:
        return {
            "label": "Unknown",
            "description": "Engine analysis is not available."
        }

    # Get the basic data
    best_move = engine_top_moves[0]
    best_winrate = best_move['winrate']
    
    user_winrate = user_move_analysis['winrate']
    user_move_coord = user_move_analysis['move']
    
    # Calculate the winrate loss
    winrate_loss = best_winrate - user_winrate
    winrate_loss_percent = round(winrate_loss * 100)

    # 1. --- Check for "Brilliant" ---
    # Condition: The move played is the best move AND
    #            there is more than one move AND
    #            the gap to the 2nd best move is significant.
    is_best_move = (user_move_coord == best_move['move'])
    if is_best_move and len(engine_top_moves) > 1:
        second_best_winrate = engine_top_moves[1]['winrate']
        gap_to_second_best = best_winrate - second_best_winrate
        
        if gap_to_second_best >= BRILLIANT_WINRATE_GAP:
            return {
                "label": "Brilliant",
                "description": f"Excellent! The only move that maintains a {round(gap_to_second_best * 100)}% advantage."
            }

    # 2. --- Check for other labels ---
    
    # "Best Move"
    if winrate_loss <= BEST_MOVE_THRESHOLD:
        return {
            "label": "Best Move",
            "description": "An optimal move!"
        }
        
    # "Good Move"
    if winrate_loss <= GOOD_MOVE_THRESHOLD:
        return {
            "label": "Good Move",
            "description": "A solid move."
        }
        
    # "Inaccuracy"
    if winrate_loss <= INACCURACY_THRESHOLD:
        return {
            "label": "Inaccuracy",
            "description": f"A bit inaccurate. You lose about {winrate_loss_percent}% winrate."
        }
        
    # "Error"
    if winrate_loss <= ERROR_THRESHOLD:
        return {
            "label": "Error",
            "description": f"Error. This move costs {winrate_loss_percent}% winrate."
        }

    # "Blunder"
    return {
        "label": "Blunder",
        "description": f"Blunder. This move loses {winrate_loss_percent}% winrate!"
    }


def get_game_phase(move_number: int) -> str:
    """
    Determines the game phase (Opening, Middlegame, Endgame)
    based on the move number.

    Args:
        move_number (int): The move number in the game (e.g., 10).

    Returns:
        str: "Opening", "Middlegame", or "Endgame".
    """
    if move_number <= OPENING_MOVES_END:
        return "Opening"
    elif move_number <= MIDGAME_MOVES_END:
        return "Middlegame"
    else:
        return "Endgame"