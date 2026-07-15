from chess.models.enums import GameTurn, PieceType


class Piece:
    ALLOWED_COLOURS = {GameTurn.BLACK.value, GameTurn.WHITE.value}
    ALLOWED_PIECES = {piece_type.value for piece_type in PieceType}

    def __init__(
        self, colour: GameTurn | str, type: PieceType | str, index: int
    ) -> None:
        if colour not in self.ALLOWED_COLOURS:
            raise ValueError(f"Colour {colour} not available")
        self.colour = GameTurn(colour).value

        try:
            self.type = PieceType(type)
        except ValueError:
            raise ValueError(f"type {type} not available")
        self.index = index
