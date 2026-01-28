WHITE = "white"
BLACK = "black"

class Piece:
    def __init__(self, color: str): # Initialize a chess piece with the given color.
        """Initialize a chess piece with the given color.
        """
        if color not in (WHITE, BLACK):
            raise ValueError("Color must be 'white' or 'black'")
        self.color = color

    def symbol(self) -> str:
        """Return the symbol representing the piece.
        """
        raise NotImplementedError("Each piece must implement its own symbol method.")
    
    def can_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Return True if this piece is allowed to move from (from_row, from_col)
        to (to_row, to_col) based on its movement rules.

        It is a DEFAULT IMPLEMANTATION!
        """
        raise NotImplementedError("Each piece must implement its own can_move method.")

    def __str__(self) -> str:
        """Return the string representation of the piece.
        """
        return self.symbol() # Return the symbol of the piece
    
class Pawn(Piece):
    """Class representing a Pawn chess piece.
    """
    def symbol(self) -> str:
        """Return the symbol representing the Pawn piece.
        """
        return 'P' if self.color == WHITE else 'p'
    
    def can_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Return True if the pawn can move from (from_row, from_col) to (to_row, to_col).
        
        White pawns move "up" the board (row decreases).
        Black pawns move "down" the board (row increases).
        """
        direction = -1 if self.color == WHITE else 1 # White: 6->5->4, Black: 1->2->3
        
        # Starting row: white pawns start at rank 2 -> row 6
        #               black pawns start at rank 7 -> row 1
        start_row = 6 if self.color == WHITE else 1

        # Move forward by 1 square and same column
        if from_col == to_col and to_row == from_row + direction:
            return True

        # Move forward by 2 squares from starting position
        if (from_col == to_col and from_row == start_row and
            to_row == from_row + 2 * direction):
            return True
        
        # Capture move (diagonal by 1 square)
        if abs(from_col - to_col) == 1 and to_row == from_row + direction:
            return True
        
        return False

class Rook(Piece):
    """Class representing a Rook chess piece.
    """
    def symbol(self) -> str:
        """Return the symbol representing the Rook piece.
        """
        return 'R' if self.color == WHITE else 'r'
    
    def can_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Return True if the rook can move from (from_row, from_col) to (to_row, to_col).
        Rooks move any number of squares along a rank or file.
        """
        # Moving along the same column
        if from_row == to_row and from_col != to_col:
            return True # Moving along the same row

        if from_col == to_col and from_row != to_row:
            return True
        
        return False

class Knight(Piece):
    """Class representing a Knight chess piece.
    """
    def symbol(self) -> str:
        """Return the symbol representing the Knight piece.
        """
        return 'N' if self.color == WHITE else 'n'
    
    def can_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Return True if the knight can move from (from_row, from_col) to (to_row, to_col).
        Knights move in an "L" shape: two squares in one direction and then one square perpendicular.
        """
        delta_row = to_row - from_row # Calculate row difference
        delta_col = to_col - from_col # Calculate column difference
        
        # Make differences positive
        if delta_row < 0:              
            delta_row = -delta_row    
        if delta_col < 0:             
            delta_col = -delta_col

        return (delta_row == 2 and delta_col == 1) or (delta_row == 1 and delta_col == 2)

class Bishop(Piece):
    """Class representing a Bishop chess piece.
    """
    def symbol(self) -> str:
        """Return the symbol representing the Bishop piece.
        """
        return 'B' if self.color == WHITE else 'b'
    
    def can_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Return True if the bishop can move from (from_row, from_col) to (to_row, to_col).
        Bishops move any number of squares diagonally.
        """
        row_diff = to_row - from_row
        col_diff = to_col - from_col

        # Cannot move if not diagonal
        if row_diff == 0 or col_diff == 0:
            return False # Not a diagonal move
        
        if row_diff < 0:
            row_diff = -row_diff
        if col_diff < 0: # We write it because it is easier to read
            col_diff = -col_diff

        return row_diff == col_diff # Diagonal move
    
class Queen(Piece):
    """Class representing a Queen chess piece.
    """
    def symbol(self) -> str:
        """Return the symbol representing the Queen piece.
        """
        return 'Q' if self.color == WHITE else 'q'
    
class King(Piece):
    """Class representing a King chess piece.
    """
    def symbol(self) -> str:
        """Return the symbol representing the King piece.
        """
        return 'K' if self.color == WHITE else 'k'    