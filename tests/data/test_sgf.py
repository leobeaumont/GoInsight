import pytest
from src.data import SgfTree, parse, serialize

@pytest.mark.parametrize("tree,expected", [
    (SgfTree({"AB": ["aa", "bb"]}, [SgfTree({"C": ["comment"]})]), True),
    (SgfTree({"C": ["root"]}), True),
])
def test_sgf_equality(tree, expected):
    """
    Test equality and inequality of SgfTree instances.
    """
    same = SgfTree(tree.properties.copy(), [SgfTree(c.properties.copy()) for c in tree.children])
    different = SgfTree({"X": ["y"]})

    assert (tree == same) == expected
    assert (tree != same) is False
    assert (tree == different) is False


@pytest.mark.parametrize("tree,expected_substring", [
    (SgfTree({"C": ["hello"]}), "(;C[hello])"),
    (SgfTree({"AB": ["aa", "bb"]}), "(;AB[aa][bb])")
])
def test_serialize(tree, expected_substring):
    """
    Test SGF serialization of a simple tree.
    """
    sgf_str = tree.to_sgf()
    assert expected_substring in sgf_str
    assert sgf_str.startswith("(")
    assert sgf_str.endswith(")")


@pytest.mark.parametrize("tree", [
    SgfTree({"C": ["Root"], "AB": ["aa"]}, [SgfTree({"B": ["bb"]}, [SgfTree({"W": ["cc"]})])])
])
def test_serialize_parse_roundtrip(tree):
    """
    Test that serializing and then parsing produces the same tree.
    """
    sgf_str = tree.to_sgf()
    parsed = parse(sgf_str)
    assert parsed == tree


def test_escape_characters():
    """
    Test escaping of special SGF characters in serialization.
    """
    tree = SgfTree({"C": ["backslash \\", "close ] bracket"]})
    sgf_str = serialize(tree)

    assert "\\\\" in sgf_str
    assert "\\]" in sgf_str

    parsed = parse("(" + sgf_str + ")")
    assert parsed.properties["C"] == ["backslash \\", "close ] bracket"]


def test_to_sgf_file(tmp_path):
    """
    Test writing SGF data to a file.
    """
    file_path = tmp_path / "out.sgf"
    tree = SgfTree({"C": ["file test"]})
    sgf_str = tree.to_sgf(str(file_path))

    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == sgf_str


def test_from_sgf_file(tmp_path):
    """
    Test reading an SGF file into an SgfTree.
    """
    path = tmp_path / "sample.sgf"
    path.write_text("(;C[test])", encoding="utf-8")

    tree = SgfTree.from_sgf(str(path))
    assert isinstance(tree, SgfTree)
    assert tree.properties == {"C": ["test"]}


def test_from_sgf_file_not_found():
    """
    Test that FileNotFoundError is raised for missing files.
    """
    error = False
    try:
        SgfTree.from_sgf("no_file_here.sgf")
    except FileNotFoundError:
        error = True
    assert error


@pytest.mark.parametrize("sgf_text", [
    ";C[test]",    # missing parentheses
    "(;c[test])",  # lowercase property
    "()"           # empty tree
])
def test_parse_invalid(sgf_text):
    """
    Test invalid SGF parsing cases.
    """
    error = False
    try:
        parse(sgf_text)
    except ValueError:
        error = True
    assert error


def test_multi_child_serialization():
    """
    Test that multiple children are serialized with proper parentheses.
    """
    child1 = SgfTree({"B": ["aa"]})
    child2 = SgfTree({"W": ["bb"]})
    root = SgfTree({"C": ["root"]}, [child1, child2])

    sgf_str = serialize(root)
    assert "(;B[aa])(;W[bb])" in sgf_str


@pytest.mark.parametrize("tree,expected", [
    (
        SgfTree({"B": ["aa"]}, [SgfTree({"W": ["bb"]}, [SgfTree({"B": ["cc"]})])]),
        ["B AA", "W BB", "B CC"]
    ),
    (
        SgfTree({"B": ["dd"]}),
        ["B DD"]
    ),
])
def test_move_sequence(tree, expected):
    """
    Test SGF move sequence extraction in GTP format.
    """
    # Minimal mock of Move.sgf_to_gtp so we don't depend on the Move module
    import src.data.sgf as sgf
    class DummyMove:
        @staticmethod
        def sgf_to_gtp(move_list):
            return move_list[0].upper()
    sgf.Move = DummyMove  # temporarily inject dummy

    result = tree.move_sequence(list_separated=False)
    assert result == expected


@pytest.mark.parametrize("tree,expected", [
    (
        SgfTree({"B": ["aa"]}, [SgfTree({"W": ["pass"]})]),
        [["B", "AA"], ["W", "PASS"]]
    ),
    (
        SgfTree({"W": ["tt"]}),
        [["W", "TT"]]
    ),
])
def test_move_sequence_list_separated(tree, expected):
    """
    Test SGF move sequence extraction with list_separated=True.
    """
    import src.data.sgf as sgf
    class DummyMove:
        @staticmethod
        def sgf_to_gtp(move_list):
            return move_list[0].upper()
    sgf.Move = DummyMove

    result = tree.move_sequence(list_separated=True)
    assert result == expected


@pytest.mark.parametrize("tree", [
    SgfTree({"C": ["no moves"]}),
    SgfTree(),
])
def test_move_sequence_empty(tree):
    """
    Test that move_sequence returns an empty list for trees without moves.
    """
    import src.data.sgf as sgf
    sgf.Move = type("Dummy", (), {"sgf_to_gtp": staticmethod(lambda x: x)})
    assert tree.move_sequence() == []


@pytest.mark.parametrize("dummy_game", [
    type("DummyGame", (), {
        "to_sgftree": lambda self: SgfTree({"C": ["dummy"]}),
        "from_sgftree": staticmethod(lambda tree: f"Game from {tree.properties}")
    })()
])
def test_from_game_and_to_game(dummy_game):
    """
    Test from_game and to_game delegation to Game methods.
    """
    import src.data.sgf as sgf
    sgf.Game = type(dummy_game)

    tree = SgfTree.from_game(dummy_game)
    assert isinstance(tree, SgfTree)
    assert tree.properties == {"C": ["dummy"]}

    result = tree.to_game()
    assert result == "Game from {'C': ['dummy']}"
