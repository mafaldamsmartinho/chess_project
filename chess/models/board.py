from typing import TYPE_CHECKING

from chess.models.enums import GameTurn, PieceType
from chess.models.piece import Piece

if TYPE_CHECKING:
    from chess.utils.serialization import SerializedBoard, SerializedPiece

NUM_ROWS: int = 8
NUM_COLS: int = 8
MAJOUR_PIECES: list[PieceType] = [
    PieceType.ROOK,
    PieceType.KNIGHT,
    PieceType.BISHOP,
    PieceType.QUEEN,
    PieceType.KING,
    PieceType.BISHOP,
    PieceType.KNIGHT,
    PieceType.ROOK,
]
INDEX_MAJOUR_PIECES: list = [1, 1, 1, 1, 1, 2, 2, 2]
SQUARE_TO_INDEX: dict[str, int] = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
}
LAST_ROW: list = ["", "a", "b", "c", "d", "e", "f", "g", "h"]
PIECES_SIMPLE: dict = {
    PieceType.PAWN: "P",
    PieceType.ROOK: "R",
    PieceType.KNIGHT: "H",
    PieceType.BISHOP: "B",
    PieceType.QUEEN: "Q",
    PieceType.KING: "K",
}
COLOUR_SIMPLE: dict = {GameTurn.BLACK: "B", GameTurn.WHITE: "W"}
ALLOWED_POSITIONS = {
    "a1",
    "a2",
    "a3",
    "a4",
    "a5",
    "a6",
    "a7",
    "a8",
    "b1",
    "b2",
    "b3",
    "b4",
    "b5",
    "b6",
    "b7",
    "b8",
    "c1",
    "c2",
    "c3",
    "c4",
    "c5",
    "c6",
    "c7",
    "c8",
    "d1",
    "d2",
    "d3",
    "d4",
    "d5",
    "d6",
    "d7",
    "d8",
    "e1",
    "e2",
    "e3",
    "e4",
    "e5",
    "e6",
    "e7",
    "e8",
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "g1",
    "g2",
    "g3",
    "g4",
    "g5",
    "g6",
    "g7",
    "g8",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "h7",
    "h8",
}


class Board:
    def __init__(self) -> None:
        """Start a board matrix 8x8."""
        self.board: list[list[Piece | None]] = [
            [None for col in range(NUM_COLS)] for row in range(NUM_ROWS)
        ]
        self.setup_board()

    def setup_board(self) -> None:
        """Setup the pieces in the board."""
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if row == 7:
                    self.board[row][col] = Piece(
                        colour=GameTurn.BLACK,
                        type=MAJOUR_PIECES[col],
                        index=INDEX_MAJOUR_PIECES[col],
                    )
                if row == 6:
                    self.board[row][col] = Piece(
                        colour=GameTurn.BLACK, type=PieceType.PAWN, index=col
                    )
                if row == 1:
                    self.board[row][col] = Piece(
                        colour=GameTurn.WHITE, type=PieceType.PAWN, index=col
                    )
                if row == 0:
                    self.board[row][col] = Piece(
                        colour=GameTurn.WHITE,
                        type=MAJOUR_PIECES[col],
                        index=INDEX_MAJOUR_PIECES[col],
                    )

    def is_valid_position(self, position: str) -> bool:
        """Check if square called is a valid position in the board."""
        return position in ALLOWED_POSITIONS

    def is_valid_position_index(self, index_position: tuple) -> bool:
        row, col = index_position
        return 0 <= row < NUM_ROWS and 0 <= col < NUM_COLS

    def position_to_index(self, position: str) -> tuple[int, int]:
        """Converts position 'a2' to index (0,1)."""
        if not self.is_valid_position(position=position):
            raise ValueError("Invalid position.")
        index = list(position)
        index_char = SQUARE_TO_INDEX[index[0]]
        index_num = int(index[1]) - 1
        return (index_num, index_char)

    def index_to_position(self, index_position: tuple[int, int]) -> str:
        """Converts index (0, 1) to position 'b1'."""
        row, col = index_position
        return f"{LAST_ROW[col + 1]}{row + 1}"

    def get_piece(self, position: str) -> Piece | None:
        """Gets piece from square."""
        sq_index = self.position_to_index(position=position)
        return self.board[int(sq_index[0])][int(sq_index[1])]

    def get_piece_by_index(self, index_position: tuple) -> Piece | None:
        """Gets piece from square index (0,1)."""
        return self.board[index_position[0]][index_position[1]]

    def set_piece(self, index_position: tuple, piece: Piece | None) -> None:
        """Sets a piece into a position."""
        self.board[index_position[0]][index_position[1]] = piece

    def move_piece(self, start: tuple, end: tuple) -> None:
        """Moves a piece from a start to an end position."""
        piece = self.get_piece_by_index(index_position=start)
        self.set_piece(index_position=start, piece=None)
        self.set_piece(index_position=end, piece=piece)

    def to_dict(self) -> "SerializedBoard":
        """Converts board into a dict of elements None or Piece."""
        board_list: SerializedBoard = []
        rows: list[SerializedPiece | None] = []
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                piece = self.board[row][col]
                if piece is None:
                    rows.append(None)
                else:
                    rows.append(
                        {
                            "colour": piece.colour,
                            "type": piece.type.value,
                            "index": piece.index,
                        }
                    )
            board_list.append(rows)
            rows = []
        return board_list
