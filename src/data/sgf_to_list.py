from sgfmill import sgf

def sgf_list(path):
    moves = []
    with open(path, "rb") as f:
        sgf_game = f.read()
    s = sgf_game.decode("utf-8")
    parts = s.split(";")
    for i in parts:
        if i[0] == "B":
            moves.append(("b",((ord(i[2])-ord('a')),ord(i[3])-ord('a'))))
        if i[0] == "W":
            moves.append(("w",((ord(i[2])-ord('a')),ord(i[3])-ord('a'))))
    return moves


