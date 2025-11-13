"""
score_graph.py

Module for visualizing game performance.
Provides tools to plot curves showing the evolution of score or win probability throughout a game.
"""

import matplotlib.pyplot as plt

def plot_win_probability(moves, win_probs):
    """
    Trace la probabilité de victoire au fil de la partie.
    moves : liste d'indices (1, 2, 3, ...)
    win_probs : liste de probabilités correspondantes (0.0 - 1.0)
    """
    plt.figure(figsize=(10, 4))
    plt.plot(moves, [p * 100 for p in win_probs], color='blue', linewidth=2)
    plt.title("Évolution de la probabilité de victoire au fil du jeu")
    plt.xlabel("Numéro du coup")
    plt.ylabel("Probabilité de victoire (%)")
    plt.ylim(0, 100)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
