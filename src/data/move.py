"""
move.py

This module handles Go moves creation, manipulation and export.

Modules:
    game -- handle manipulation and encoding of games.
    move -- handle manipulation and encoding of moves.
"""

class Move:
    """
    Stores move's data.

    Args:
        argname (argtype): Description of the arg. 

    Attributes:
        attrname (attrtype): Attribut description.

    Methods:
        to_gtp(): Export move to the gtp format.
    """

    def __init__(self):
        pass
    
    def to_gtp(self) -> str:
        """
        Translate the move to the gtp format.
        
        Returns:
            (str): the move in gtp format.
        """
        pass
