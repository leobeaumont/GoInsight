"""
game.py

This module handles Go games import, manipulation and export.

Modules:
    game -- handle manipulation and encoding of games.
    move -- handle manipulation and encoding of moves.
"""

class Game:
    """
    Manages game's data with various tools.

    Args:
        argname (argtype): Description of the arg. 

    Attributes:
        attrname (attrtype): Attribut description.

    Methods:
        from_sgf(path): Create a Game object from an sgf file.
    """

    def __init__(self):
        pass
    
    @classmethod
    def from_sgf(cls, path: str) -> "Game":
        """
        Create a new Game object from an sgf file.

        Args:
            path (str): Path to the sgf file.

        Raises:
            FileNotFoundError: If the sgf file is not found.
        
        Returns:
            (Game): the game provided in the sgf file.
        """
        pass
