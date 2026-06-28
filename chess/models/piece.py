class Piece:
    ALLOWED_COLOURS = {'black', 'white'}
    ALLOWED_PIECES = {'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'}

    def __init__(self, colour: str, type: str, index: int) -> None:
        if colour not in self.ALLOWED_COLOURS:
            raise ValueError(f'Colour {colour} not available')
        self.colour = colour

        if type not in self.ALLOWED_PIECES:
            raise ValueError(f'type {type} not available')
        self.type = type
        self.index = index
