WHITE = "white"
BLACK = "black"

class Piece:
    def __init__(self, color: str):
        """Initialize a chess piece with the given color.
        """
        if color not in (WHITE, BLACK):
            raise ValueError("Color must be 'white' or 'black'")
        self.color = color

    def symbol(self) -> str:
        """Return the symbol representing the piece.
        """
        raise NotImplementedError("Each piece must implement its own symbol method.")
    
    def __str__(self) -> str:
        """Return the string representation of the piece.
        """
        return self.symbol()
    
class Pawn(Piece):
    """Class representing a Pawn chess piece.
    """
    def symbol(self) -> str:
        """Return the symbol representing the Pawn piece.
        """
        return 'P' if self.color == WHITE else 'p'
    
class Rook(Piece):
    """Class representing a Rook chess piece.
    """
    def symbol(self) -> str:
        """Return the symbol representing the Rook piece.
        """
        return 'R' if self.color == WHITE else 'r'
    
class Knight(Piece):
    """Class representing a Knight chess piece.
    """
    def symbol(self) -> str:
        """Return the symbol representing the Knight piece.
        """
        return 'N' if self.color == WHITE else 'n'
    
class Bishop(Piece):
    """Class representing a Bishop chess piece.
    """
    def symbol(self) -> str:
        """Return the symbol representing the Bishop piece.
        """
        return 'B' if self.color == WHITE else 'b'
    
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