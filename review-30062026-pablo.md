# Comment 1
Possible to handle database connections from a database manager

# Comment 2
# Locate functions properly under the file that has its proper ownership

# Comment 3
Substitute if possible sql tables definition with modern ORM defined models

# Comment 4
Substitute raw SQL queries with sqlalquemy lib wrapper queries.

# Comment 5
# Encapsulate each repository set of operations under a different file to maintain ownership.
# In case that is there any mixed query, keep it in in teh repo where the ultimate data is coming from.

# Comment 6
# Improve function naming (e.g. get_players -> get_players_by_game_id)

# Comment 7
# Include annotations in ALL functions.

# Comment 8
# Add enums instead of hardcoding in: GameStatus, PieceType, etc

# Comment 9
Review is_valid_move function for redundant checks.

# Comment 10
<!-- Include parameters in Game initialization.
def __init__(self, turn, status) -> None:
        """Initialises the game"""
        self.board = Board()
        self.turn = turn
        self.status = status

    def set_board(self, board):
        self.board = board -->

# Comment 11
# Use "=" when calling a function

# Comment 12
# move out of bot service the game service responsibility operations (call make move instead of database related calls.)

# Comment 13
# TODO apply pydantic instantiation
<!-- def deserialize_board(data) -> Board:
    """Converts json board into a board list of el None or Piece"""
    board = Board()
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el is not None:
                colour = el.get('colour')
                type = el.get('type')
                index = el.get('index')
                board.board[i][j] = Piece(colour, type, index)
            else:
                board.board[i][j] = None
    return board -->