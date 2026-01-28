from chessgame.types import square_to_position, position_to_square

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

    def is_empty(self, square: str) -> bool:
        """Check if the given chess square is empty.
        """
        return self.get_piece(square) is None # Return True if no piece is present

    def is_opponent_piece(self, square: str, color: str) -> bool:
        """Check if the piece at the given square belongs to the opponent.
        """
        piece = self.get_piece(square)         # Get the piece at the square
        
        if piece is None:                      # If no piece is present
            return False                       # Return False
        
        return piece.color != color            # Return True if colors differ
    
    def find_king(self, color: str) -> str | None:
        """Find the square of the king of the given color.
        """
        from chessgame.pieces import King # Import here to avoid circular imports

        for row in range(8):         # Go through each row
            for col in range(8):     # Go through each column
                piece = self.grid[row][col]
                
                if piece is not None and isinstance(piece, King) and piece.color == color:
                    return position_to_square((row, col)) # Return the square of the king
        
        return None # King not found 

    def is_square_under_attack(self, target_square: str, attacker_color: str) -> bool:
        """Check if the target square is under attack by any piece of the attacker_color.
        """
        from chessgame.pieces import Pawn, Rook, Bishop, Knight, Queen, King, WHITE, BLACK

        # Determine which color is attacking
        target_row, target_col = square_to_position(target_square)

        for r in range(8):                        # Go through each row
            for c in range(8):                    # Go through each column
                piece = self.grid[r][c]           # Get the piece at (r, c)
                if piece is None:                 # No piece present
                    continue                      # Skip to next square
                if piece.color != attacker_color: # Not an attacking piece
                    continue                      # Skip to next square

                # Pawn attacks are special: only diagonals (not forward)
                if isinstance(piece, Pawn):
                    direction = -1 if piece.color == WHITE else 1      # white pawns go up, black pawns go down
                    col_diff = target_col - c                          # Calculate column difference
                    if col_diff < 0:                                   # If the column difference is negative
                        col_diff = -col_diff                           # Make it positive

                    if target_row == r + direction and col_diff == 1:
                        return True
                    continue

                # Knight + King attacks are just their shape rules
                if isinstance(piece, Knight) or isinstance(piece, King):
                    if piece.can_move(r, c, target_row, target_col):
                        return True
                    continue

                # Sliding pieces (rook/bishop/queen) need clear path
                if isinstance(piece, Rook) or isinstance(piece, Bishop) or isinstance(piece, Queen):
                    if not piece.can_move(r, c, target_row, target_col):
                        continue

                    dr = target_row - r
                    dc = target_col - c

                    step_row = 0 if dr == 0 else (1 if dr > 0 else -1)
                    step_col = 0 if dc == 0 else (1 if dc > 0 else -1)

                    cur_row = r + step_row
                    cur_col = c + step_col

                    while cur_row != target_row or cur_col != target_col:
                        # Check if any piece blocks the path
                        if self.grid[cur_row][cur_col] is not None:
                            break
                        cur_row += step_row
                        cur_col += step_col
                    else:
                        # The while loop ended normally no break => no blocking
                        return True

        return False

    def is_in_check(self, color: str) -> bool:
        """Check if the king of the given color is in check.
        """
        from chessgame.pieces import WHITE, BLACK

        king_square = self.find_king(color) # Find the king's square

        if king_square is None:             # If king not found
            return False                    # Cannot be in check

        opponent_color = BLACK if color == WHITE else WHITE
        return self.is_square_under_attack(king_square, opponent_color)

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

    def move_piece(self, from_square: str, to_square: str, turn_color: str) -> bool:
        """Move a piece from one square to another, if it belongs to the current player's color.
        Returns True if the move was successful, False otherwise."""
        piece = self.get_piece(from_square) # Get the piece at the source square
        
        if piece is None: # Must be a piece to move
            return False  # No piece to move
        
        if piece.color != turn_color: # Check if the piece belongs to the current player
            return False              # Cannot move opponent's piece

        from_row, from_col = square_to_position(from_square)
        to_row, to_col = square_to_position(to_square)

        # Check if the piece can move according to its movement rules
        if not piece.can_move(from_row, from_col, to_row, to_col):
            return False # Move not allowed by piece rules

        # Check for Pawn movement rules
        from chessgame.pieces import Pawn # We import here to avoid circular imports

        if isinstance(piece, Pawn):
            target_piece = self.get_piece(to_square) # Get the piece at the destination square

            if from_col == to_col: # Moving forward 
                if target_piece is not None:
                    return False # Cannot move forward to an occupied square
               
                # Check if the square in between is empty
                if abs(to_row - from_row) == 2: # Double move
                    middle_row = (from_row + to_row) // 2
                    middle_square = position_to_square((middle_row, from_col))
                    if self.get_piece(middle_square) is not None:
                        return False # Cannot jump over a piece
            
            else: # Capturing diagonally
                if target_piece is None:
                    return False # Cannot move diagonally without capturing
                if target_piece.color == piece.color:
                    return False # Cannot capture own piece

        # Check for Rook movement blocking
        if piece.__class__.__name__ == "Rook":
            # Determine direction of movement (step_row, step_col)
            if from_row == to_row:
                step_row = 0
                step_col = 1 if to_col > from_col else -1
            else:
                step_col = 0
                step_row = 1 if to_row > from_row else -1

            # Walk squares between start and destination 
            cur_row = from_row + step_row
            cur_col = from_col + step_col

            while (cur_row, cur_col) != (to_row, to_col):
                middle_square = position_to_square((cur_row, cur_col))
                if self.get_piece(middle_square) is not None:
                    return False  # blocked

                cur_row += step_row
                cur_col += step_col

            # Final square cannot capture your own piece
            target_piece = self.get_piece(to_square)
            if target_piece is not None and target_piece.color == piece.color:
                return False
        
        # Check for Knight movement capturing own piece
        from chessgame.pieces import Knight # Import here to avoid circular imports

        if isinstance(piece, Knight): # Knight movement
            target_piece = self.get_piece(to_square)
            if target_piece is not None and target_piece.color == piece.color:
                return False

        # Check for Bishop movement blocking
        if piece.__class__.__name__ == "Bishop":
            step_row = 1 if to_row > from_row else -1
            step_col = 1 if to_col > from_col else -1

            cur_row = from_row + step_row
            cur_col = from_col + step_col

            # Walk diagonally until destination 
            while cur_row != to_row or cur_col != to_col:
                middle_square = position_to_square((cur_row, cur_col))

                # If we are at destination, stop checking middle squares
                if middle_square == to_square:
                    break

                if self.get_piece(middle_square) is not None:
                    return False  # blocked

                cur_row += step_row
                cur_col += step_col

            # Destination cannot capture your own piece
            target_piece = self.get_piece(to_square)
            if target_piece is not None and target_piece.color == piece.color:
                return False
            
        # Check for Queen movement blocking
        from chessgame.pieces import Queen # Import here to avoid circular imports

        if isinstance(piece, Queen):
            delta_row = to_row - from_row
            delta_col = to_col - from_col

            # Determine direction of movement
            step_row = 0 if delta_row == 0 else (1 if delta_row > 0 else -1)
            step_col = 0 if delta_col == 0 else (1 if delta_col > 0 else -1)

            # Walk squares between start and destination
            cur_row = from_row + step_row
            cur_col = from_col + step_col

            # Walk squares between start and destination
            while (cur_row, cur_col) != (to_row, to_col):
                middle_square = position_to_square((cur_row, cur_col))
                if self.get_piece(middle_square) is not None:
                    return False  # blocked

                # Move to next square in the path
                cur_row += step_row
                cur_col += step_col

            # Final square cannot capture your own piece
            target_piece = self.get_piece(to_square)
            if target_piece is not None and target_piece.color == piece.color:
                return False
        
        # Check for King movement capturing own piece
        from chessgame.pieces import King # Import here to avoid circular imports

        if isinstance(piece, King):
            target_piece = self.get_piece(to_square)
            if target_piece is not None and target_piece.color == piece.color:
                return False
        
        # Save what is currently on the destination square 
        captured_piece = self.get_piece(to_square)

        # Make the move temporarily
        self.set_piece(to_square, piece)
        self.set_piece(from_square, None)

        # Illegal if it leaves your king in check
        if self.is_in_check(turn_color):
            self.set_piece(from_square, piece) # Undo the move
            self.set_piece(to_square, captured_piece)
            return False

        return True