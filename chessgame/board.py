from chessgame.types import square_to_position

class Board: # ChessBoard 8x8 grid
    """Class representing an 8x8 chess board.
    """
    def __init__(self):
        """Create an 8x8 chess board initialized with None values.
        """
        self.grid = [] # Create an empty board

        for r in range(8):            # 8 rows
            row_list = []             # Create an empty row
            for c in range(8):        # 8 columns
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

    def print_board(self) -> None:
        """Print the current state of the chess board.
        """
        # print column letters which we start with 2 spaces so it aligns with the rows
        print("  a b c d e f g h") 

        # Print each row and go through each row index
        for row in range(8):
            rank = 8 - row         # Calculate the rank number (8 to 1)
            line = str(rank) + " " # Start the line with the rank number

            for col in range(8): # Go through each column index (0 to 7)
                piece = self.grid[row][col]
                
                 # If square is empty, print a dot
                if piece is None:
                    line += ". "
                else: # Otherwise print the piece
                    line += str(piece) + " "

            print(line + str(rank))

        print("  a b c d e f g h") # Bottom labels

    def setup_starting_position(self) -> None:
        """Set up the chess board with the standard starting position.
        """
        from chessgame.pieces import (King, Pawn, Rook, Knight, Bishop, Queen, WHITE, BLACK)

        # Pawns
        for file in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            self.set_piece(file + "2", Pawn(WHITE))
            self.set_piece(file + "7", Pawn(BLACK))

        # White back rank
        self.set_piece("a1", Rook(WHITE))
        self.set_piece("b1", Knight(WHITE))
        self.set_piece("c1", Bishop(WHITE))
        self.set_piece("d1", Queen(WHITE))
        self.set_piece("e1", King(WHITE))
        self.set_piece("f1", Bishop(WHITE))
        self.set_piece("g1", Knight(WHITE))
        self.set_piece("h1", Rook(WHITE))

        # Black back rank
        self.set_piece("a8", Rook(BLACK))
        self.set_piece("b8", Knight(BLACK))
        self.set_piece("c8", Bishop(BLACK))
        self.set_piece("d8", Queen(BLACK))
        self.set_piece("e8", King(BLACK))
        self.set_piece("f8", Bishop(BLACK))
        self.set_piece("g8", Knight(BLACK))
        self.set_piece("h8", Rook(BLACK))