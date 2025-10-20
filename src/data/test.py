from .game import Game
from .move import Move

game = Game(size=9)

move1 = Move(game, 'b', (3, 3))
game.play_move(move1)
print(game)

move2 = Move(game, 'w', None)
game.play_move(move2)

print(game)
