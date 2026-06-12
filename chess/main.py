from chess.services.game_service import play_move
from chess.models.game import Game

next_turn = 'white'
game = Game()

while next_turn is not None:
    game.board.to_display()
    print('Next turn: ', next_turn)
    start = input('Piece to move: ')
    while not game.board.is_valid_position(start):
        print(f'{start} square not valid')
        start = input('Piece to move: ')

    end = input('Destination Square: ')
    while not game.board.is_valid_position(end):
        print(f'{end} square not valid')
        end = input('Destination Square: ')

    play: dict = play_move(game, start, end)
    next_turn = play.get("next_turn")
    print(play.get("message"), '\n')
