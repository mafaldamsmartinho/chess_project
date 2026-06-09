# from enum import StrEnum


# class PieceType(StrEnum):
#     PAWN = 'pawn'


class Piece:
    ALLOWED_COLOURS = {'black', 'white'}
    ALLOWED_PIECES = {'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'}

    def __init__(self, colour: str, type: str, index: int):
        if colour not in self.ALLOWED_COLOURS:
            raise ValueError(f'Colour {colour} not available')
        self.colour = colour

        if type not in self.ALLOWED_PIECES:
            raise ValueError(f'type {type} not available')
        self.type = type
        self.index = index

    # PRIVATE METHODS (TO BE USED JUST WITHIN THE CLASS)
    def __str__(self):
        return f"{self.colour} {self.type} {self.index}"

    def to_dict(self):
        return self.__dict__
