import pytest
from score_graph import plot_win_probability

def test_plot_win_probability_basic():
    """
    Test basic plotting with a small set of moves and win probabilities.
    Ensures the function runs without errors.
    """
    moves = list(range(1, 11))  # coups 1 à 10
    win_probs = [0.5, 0.52, 0.48, 0.55, 0.60, 0.58, 0.63, 0.65, 0.62, 0.70]

    # The test passes if the plot function executes without exceptions
    try:
        plot_win_probability(moves, win_probs)
    except Exception as e:
        pytest.fail(f"plot_win_probability raised an exception: {e}")

def test_plot_win_probability_empty():
    """
    Test plotting with empty data.
    The function should handle empty lists gracefully.
    """
    moves = []
    win_probs = []

    try:
        plot_win_probability(moves, win_probs)
    except Exception as e:
        pytest.fail(f"plot_win_probability raised an exception with empty data: {e}")

def test_plot_win_probability_single_point():
    """
    Test plotting with a single move.
    """
    moves = [1]
    win_probs = [0.5]

    try:
        plot_win_probability(moves, win_probs)
    except Exception as e:
        pytest.fail(f"plot_win_probability raised an exception with single data point: {e}")
