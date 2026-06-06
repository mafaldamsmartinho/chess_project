class Piece:
    ALLOWED_COLOURS = {'black', 'white'}
    ALLOWED_PIECES = {'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'}

    def __init__(self, colour: str, piece: str):
        if colour not in self.ALLOWED_COLOURS:
            raise ValueError(f'Colour {colour} not available')
        self.colour = colour

        if piece not in self.ALLOWED_PIECES:
            raise ValueError(f'Piece {piece} not available')
        self.piece = piece


