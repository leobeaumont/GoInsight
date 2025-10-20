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
