# main.py

from .game import Game
from .move import Move

def main():
    game = Game(size=9)
    print("Welcome to Go! (enter moves like 'D4' or 'pass')")

    while not game.ended:
        print(game)
        color = game.next_color()
        move_str = input(f"{color.upper()}'s move: ").strip().upper()

        if move_str == "PASS":
            move = Move(game, color, None)
        else:
            try:
                col_letter = move_str[0]
                row_number = int(move_str[1:])
                x = "ABCDEFGHJKLMNOPQRSTUVWXYZ".index(col_letter)
                y = row_number - 1
                move = Move(game, color, (x, y))
            except Exception:
                print("Invalid move format. Example: D4 or pass")
                continue

        try:
            game.play_move(move)
        except ValueError as e:
            print(e)
            continue

    # End of game
    print("\nGame Over!")
    print(game.board)
    scores = game.score()
    print(f"Scores → Black: {scores['b']} | White: {scores['w']}")
    print(f"Winner: {game.winner().upper()}")

if __name__ == "__main__":
    main()
