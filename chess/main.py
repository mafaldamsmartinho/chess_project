from chess.services.game_service import play_move
from chess.models.game import Game

next_turn = 'white'
game = Game()

while next_turn is not None:
    print('Next turn: ', next_turn)
    start = input('Piece to move: ')
    end = input('Destination Square: ')

    if start == 'exit' or end == 'exit':
        break

    play: dict = play_move(game, start, end)
    next_turn = play.get("next_turn")
    print(play.get("message"))
