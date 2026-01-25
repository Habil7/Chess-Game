from chessgame.types import square_to_position

class Board: # ChessBoard 8x8 grid
    """Class representing an 8x8 chess board.
    """
    def __init__(self):
        """Create an 8x8 chess board initialized with None values.
        """
        self.grid = [] # Create an empty board

        for r in range(8): # 8 rows
            row_list = [] # Create an empty row
            for c in range(8): # 8 columns
                row_list.append(None) # Initialize each square to None

            self.grid.append(row_list) # Add the row to the grid
    def get_piece(self, square: str):
        """Return the piece at the given chess square.
        """
        row, col = square_to_position(square)  # Convert square to (row, col)
        return self.grid[row][col]             # Return the piece at that position

    def set_piece(self, square: str, piece) -> None:
        """Set the piece at the given chess square.
        """
        row, col = square_to_position(square)  # Convert square to (row, col)
        self.grid[row][col] = piece            # Set the piece at that position