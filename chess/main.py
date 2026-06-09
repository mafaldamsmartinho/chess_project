from chess.services.game_service import play_move
from chess.models.game import Game

next_turn = 'white'
game = Game()

while next_turn is not None:
    print(game.board.to_display())
    print('Next turn: ', next_turn)
    start = input('Piece to move: ')
    if not game.board.is_valid_position(start):
        print(f'{start} square not valid')
        start = input('Piece to move: ')       
    end = input('Destination Square: ')
    if not game.board.is_valid_position(end):
        print(f'{end} square not valid')
        end = input('Destination Square: ')

    if start == 'exit' or end == 'exit':
        print("Bye... See you soon.")
        break

    play: dict = play_move(game, start, end)
    next_turn = play.get("next_turn")
    play.get("message")
