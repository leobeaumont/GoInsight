"""
sgf.py

This module handles translations between SGF encodings and SGF trees.

Modules:
    board -- handle manipulation and encoding of the board.
    game  -- handle manipulation and encoding of games.
    move  -- handle manipulation and encoding of moves.
    sgf   -- handle SGF parsing.
"""

import os

class SgfTree:
    """Represents a node in an SGF (Smart Game Format) tree.

    Each SGF tree node may contain a set of properties and a list of child nodes.

    Attributes:
        properties (dict): A dictionary mapping property names (str) to lists of values (list[str]).
        children (list[SgfTree]): A list of child SgfTree nodes.
    """

    def __init__(self, properties=None, children=None):
        """Initialize a new SgfTree instance.

        Args:
            properties (dict, optional): A dictionary of SGF properties. Defaults to an empty dict.
            children (list[SgfTree], optional): A list of child nodes. Defaults to an empty list.
        """
        self.properties = properties or {}
        self.children = children or []

    def __eq__(self, other):
        """Compare two SgfTree instances for equality.

        Args:
            other (SgfTree): Another SgfTree instance to compare with.

        Returns:
            bool: True if both trees have identical properties and children, False otherwise.
        """
        if not isinstance(other, SgfTree):
            return False
        for key, value in self.properties.items():
            if key not in other.properties:
                return False
            if other.properties[key] != value:
                return False
        for key in other.properties.keys():
            if key not in self.properties:
                return False
        if len(self.children) != len(other.children):
            return False
        for child, other_child in zip(self.children, other.children):
            if child != other_child:
                return False
        return True

    def __ne__(self, other):
        """Check if two SgfTree instances are not equal.

        Args:
            other (SgfTree): Another SgfTree instance to compare with.

        Returns:
            bool: True if the two trees are not equal, False otherwise.
        """
        return not self == other
    
    @classmethod
    def from_sgf(cls, path: str) -> "SgfTree":
        """Create an SgfTree instance from an SGF file.

        This method reads an SGF file from the given path and parses its content into an SgfTree structure.

        Args:
            path (str): The filesystem path to the SGF file.

        Returns:
            SgfTree: The root node of the parsed SGF tree.

        Raises:
            FileNotFoundError: If the file does not exist or cannot be accessed.
            ValueError: If the SGF file content is invalid and cannot be parsed.
        """
        if not os.path.isfile(path):
            raise FileNotFoundError(f"The specified SGF file was not found: '{path}'")

        with open(path, "r", encoding="utf-8") as file:
            sgf_data = file.read()

        return parse(sgf_data)



def parse(input):
    """Parse an SGF string into an SgfTree object.

    This function parses the textual SGF format and returns the corresponding
    SgfTree representation. It validates the syntax and raises ValueError on malformed input.

    Args:
        input (str): The SGF-formatted input string.

    Returns:
        SgfTree: The root node of the parsed SGF tree.

    Raises:
        ValueError: If the SGF format is invalid, such as:
            - Missing tree delimiters.
            - Lowercase property names.
            - Improper property delimiters.
            - Empty trees or malformed nodes.
    """
    pos = 1

    def get_property():
        """Parse a single SGF property and its values.

        Returns:
            dict: A dictionary containing one property name and its list of values.

        Raises:
            ValueError: If property syntax is invalid (e.g., lowercase name, missing delimiters).
        """
        nonlocal pos
        ind = pos
        while input[ind].isupper():
            ind += 1
        if input[ind].islower():
            raise ValueError('property must be in uppercase')
        if input[ind] != '[':
            raise ValueError('properties without delimiter')
        key = input[pos:ind]
        prop = {key: []}
        pos = ind
        while input[pos] == '[':
            pos = ind = pos + 1
            w = []
            while input[ind] != ']':
                if input[ind] == '\t':
                    w.append(' ')
                elif input[ind:ind + 2] in ('\\]', '\\\\'):
                    w.append(input[ind + 1])
                    ind += 1
                elif input[ind:ind + 2] == '\\\n':
                    ind += 1
                elif input[ind] != '\\':
                    w.append(input[ind])
                ind += 1
            prop[key].append(''.join(w))
            pos = ind + 1
        return prop
    
    def get_node():
        """Recursively parse a single SGF node and its children.

        Returns:
            SgfTree: The parsed node with properties and subtrees.

        Raises:
            ValueError: If the SGF tree contains empty nodes or malformed structure.
        """
        nonlocal pos
        properties = {}
        children = []
        while input[pos] == '(':
            pos += 1
        if input[pos] == ')':
            raise ValueError('tree with no nodes')
        pos += 1
        while input[pos] not in ('(', ')', ';'):
            properties.update(get_property())
        while pos < len(input) and input[pos] != ')':
            children.append(get_node())
        pos += 1
        return SgfTree(properties, children)  
        
    if not input.startswith('('):
        raise ValueError('tree missing')
    return get_node()
