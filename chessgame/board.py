# Chess Game Board Module
from chessgame.types import square_to_position, position_to_square

# ChessBoard Class
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

        # We track en passant target square here if needed.
        # It only happens when a pawn moves two squares from its starting position.
        # An enemy pawn next to it can capture as if it moved only one square.
        # This capture is only allowed immediately on the next move.
        self.en_passant_target = None # No en passant target square initially

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

    def try_move_no_turn_switch(self, from_square: str, to_square: str, turn_color: str) -> bool:
        """Try to move a piece from one square to another without switching turns.
        Returns True if the move was successful, False otherwise.
        """
        if from_square == to_square: # Cannot move to the same square
            return False
        
        from_piece = self.get_piece(from_square)
        if from_piece is None or from_piece.color != turn_color:
            return False # No piece to move or not the player's piece
        
        to_piece_before = self.get_piece(to_square)
        if to_piece_before is not None and to_piece_before.color == turn_color:
            return False # Cannot capture own piece
        
        # Save current state to restore later
        old_has_moved = from_piece.has_moved           # Save current has_moved status
        old_en_passant_target = self.en_passant_target # Save current en passant target
        
         # Track possible en passant capture removal so we can restore it
        captured_ep_square = None
        captured_ep_piece = None

        from chessgame.pieces import Pawn, King, WHITE

        # If this try-move is an en passant capture, the captured pawn is NOT on to_square.
        # It sits behind the target square at (from_row, to_col).
        if isinstance(from_piece, Pawn):
            from_row, from_col = square_to_position(from_square)
            to_row, to_col = square_to_position(to_square)

            if from_col != to_col and to_piece_before is None and old_en_passant_target == to_square:
                captured_ep_square = position_to_square((from_row, to_col))
                captured_ep_piece = self.get_piece(captured_ep_square)

        # Track castling rook movement so we can undo it too
        castling = False
        rook_square = None
        rook_to_square = None
        old_rook_has_moved = None

        if isinstance(from_piece, King):
            from_row, from_col = square_to_position(from_square)
            to_row, to_col = square_to_position(to_square)
            
            if from_row == to_row and abs(to_col - from_col) == 2:
                castling = True
                kingside = to_col > from_col

                if turn_color == WHITE:
                    rook_square = "h1" if kingside else "a1"
                    rook_to_square = "f1" if kingside else "d1"
                else:
                    rook_square = "h8" if kingside else "a8"
                    rook_to_square = "f8" if kingside else "d8"

                # We don't yet know if castle succeeds, so we also save the rook at original square now:
                rook_at_start = self.get_piece(rook_square)
                if rook_at_start is not None:
                    old_rook_has_moved = rook_at_start.has_moved

        moved = self.move_piece(from_square, to_square, turn_color)
        if not moved:
            from_piece.has_moved = old_has_moved           # Restore has_moved status
            self.en_passant_target = old_en_passant_target # Restore en passant target
            return False                                   # Move was not successful
        
        # Save rook AFTER move 
        rook_after = None
        if castling and rook_to_square is not None:
            rook_after = self.get_piece(rook_to_square)

        self.set_piece(from_square, from_piece) # Undo the move
        self.set_piece(to_square, to_piece_before)     # Restore captured piece if any

        # If en passant capture removed a pawn, restore it
        if captured_ep_square is not None:
            self.set_piece(captured_ep_square, captured_ep_piece)

        # If castling happened, restore rook back to its original square
        if castling and rook_square is not None and rook_to_square is not None and rook_after is not None:
            self.set_piece(rook_square, rook_after)
            self.set_piece(rook_to_square, None)
             # Restore rook has_moved if we saved it
            if old_rook_has_moved is not None:
                rook_after.has_moved = old_rook_has_moved

        from_piece.has_moved = old_has_moved           # Restore has_moved status
        self.en_passant_target = old_en_passant_target # Restore en passant target

        return True # Move was successful

    def has_any_legal_move(self, color: str) -> bool:
        """Check if the player of the given color has any legal moves.
        """
        for from_row in range(8):         # Go through each row
            for from_col in range(8):     # Go through each column
                piece = self.grid[from_row][from_col]
                if piece is None or piece.color != color:
                    continue # No piece or not player's piece

                from_square = position_to_square((from_row, from_col))

                for to_row in range(8):       # Go through each row for destination
                    for to_col in range(8):   # Go through each column for destination
                        to_square = position_to_square((to_row, to_col))

                        if self.try_move_no_turn_switch(from_square, to_square, color):
                            return True # Found a legal move

        return False # No legal moves found

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
                    direction = -1 if piece.color == WHITE else 1      # White pawns go up, black pawns go down
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
                    else: # The while loop ended normally no break => no blocking
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

    def is_checkmate(self, color: str) -> bool:
        """Check if the player of the given color is in checkmate.
        """
        if not self.is_in_check(color): # Not in check
            return False                # Cannot be checkmate

        if self.has_any_legal_move(color): # Has legal moves
            return False                    # Cannot be checkmate

        return True # In check and no legal moves => checkmate

    def is_stalemate(self, color: str) -> bool:
        """Check if the player of the given color is in stalemate.
        """
        if self.is_in_check(color): # In check
            return False            # Cannot be stalemate

        if self.has_any_legal_move(color): # Has legal moves
            return False                    # Cannot be stalemate

        return True # Not in check and no legal moves => stalemate

    def set_piece(self, square: str, piece) -> None:
        """Set the piece at the given chess square.
        """
        row, col = square_to_position(square)  # Convert square to (row, col)
        self.grid[row][col] = piece            # Set the piece at that position

    def print_board(self) -> None:
        """Print the current state of the chess board.
        """
        # Print column letters which we start with 2 spaces so it aligns with the rows
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

    def try_castle(self, from_square: str, to_square: str, turn_color: str) -> bool:
        """Attempt to castle (king moves 2 squares).
        Returns True if castling is legal and performed, otherwise False.
        """
        from chessgame.pieces import King, Rook, WHITE, BLACK

        king = self.get_piece(from_square)
        if king is None or not isinstance(king, King) or king.color != turn_color:
            return False

        # King must not have moved
        if king.has_moved:
            return False

        from_row, from_col = square_to_position(from_square)
        to_row, to_col = square_to_position(to_square)

        # Must be same row and exactly 2 columns
        if from_row != to_row or abs(to_col - from_col) != 2:
            return False

        # King cannot castle out of check
        if self.is_in_check(turn_color):
            return False

        # Determine side
        kingside = to_col > from_col

        # Rook square and squares between
        if turn_color == WHITE:
            rook_square = "h1" if kingside else "a1"
            king_path_squares = ["f1", "g1"] if kingside else ["d1", "c1"]
            between_squares = ["f1", "g1"] if kingside else ["b1", "c1", "d1"]
            rook_to_square = "f1" if kingside else "d1"
        else:
            rook_square = "h8" if kingside else "a8"
            king_path_squares = ["f8", "g8"] if kingside else ["d8", "c8"]
            between_squares = ["f8", "g8"] if kingside else ["b8", "c8", "d8"]
            rook_to_square = "f8" if kingside else "d8"

        rook = self.get_piece(rook_square)
        if rook is None or not isinstance(rook, Rook) or rook.color != turn_color:
            return False

        # Rook must not have moved
        if rook.has_moved:
            return False

        # Squares between king and rook must be empty
        for sq in between_squares:
            if self.get_piece(sq) is not None:
                return False

        # Squares the king passes through (and destination) must not be under attack
        opponent_color = BLACK if turn_color == WHITE else WHITE

        for sq in king_path_squares:
            if self.is_square_under_attack(sq, opponent_color):
                return False

        # Perform castling
        self.set_piece(to_square, king)
        self.set_piece(from_square, None)

        self.set_piece(rook_to_square, rook)
        self.set_piece(rook_square, None)

        # Safety undo if still in check
        if self.is_in_check(turn_color):
            self.set_piece(from_square, king)
            self.set_piece(to_square, None)
            self.set_piece(rook_square, rook)
            self.set_piece(rook_to_square, None)
            return False

        # Mark both as moved
        king.has_moved = True
        rook.has_moved = True

        return True

    def move_piece(self, from_square: str, to_square: str, turn_color: str) -> bool:
        """Move a piece from one square to another, if it belongs to the current player's color.
        Returns True if the move was successful, False otherwise."""
        piece = self.get_piece(from_square) # Get the piece at the source square
        
        from chessgame.pieces import King, Pawn, Queen, Knight, WHITE, BLACK
        
        if piece is None: # Must be a piece to move
            return False  # No piece to move
        
        if piece.color != turn_color: # Check if the piece belongs to the current player
            return False              # Cannot move opponent's piece

        from_row, from_col = square_to_position(from_square)
        to_row, to_col = square_to_position(to_square)

        # Save en passant state from previous move   
        old_en_passant_target = self.en_passant_target
        
        # Reset by default: en passant target only exists for ONE move after a pawn double-step
        self.en_passant_target = None

        # Helper: any failed move must restore old en passant target
        def fail() -> bool:
            self.en_passant_target = old_en_passant_target
            return False
        
        # Handle castling BEFORE normal can_move check (because king.can_move doesn't allow 2 squares)
        if isinstance(piece, King):
            if from_row == to_row and abs(to_col - from_col) == 2:
                if self.try_castle(from_square, to_square, turn_color):
                    return True
                return fail()
    
        # Check if the piece can move according to its movement rules
        if not piece.can_move(from_row, from_col, to_row, to_col):
            return fail() # Move not allowed by piece rules

        if isinstance(piece, Pawn):
            target_piece = self.get_piece(to_square) # Get the piece at the destination square

            if from_col == to_col: # Moving forward 
                if target_piece is not None:
                    return fail() # Cannot move forward to an occupied square
               
                # Check if the square in between is empty
                if abs(to_row - from_row) == 2: # Double move
                    middle_row = (from_row + to_row) // 2
                    middle_square = position_to_square((middle_row, from_col))
                    
                    if self.get_piece(middle_square) is not None:
                        return fail() # Cannot jump over a piece

                    # Store the square that can be captured via en passant on the next move
                    self.en_passant_target = middle_square 

            else: # Capturing diagonally
                if target_piece is None:
                    # Allow en passant only if landing square equals previous target
                    if old_en_passant_target != to_square:
                        return fail() # Cannot move diagonally without capturing
                else:
                    if target_piece.color == piece.color:
                        return fail() # Cannot capture own piece

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
                    return fail()  # blocked

                cur_row += step_row
                cur_col += step_col

            # Final square cannot capture your own piece
            target_piece = self.get_piece(to_square)
            if target_piece is not None and target_piece.color == piece.color:
                return fail()
        
        if isinstance(piece, Knight): # Knight movement
            target_piece = self.get_piece(to_square)
            if target_piece is not None and target_piece.color == piece.color:
                return fail()

        # Check for Bishop movement blocking
        if piece.__class__.__name__ == "Bishop":
            step_row = 1 if to_row > from_row else -1
            step_col = 1 if to_col > from_col else -1

            cur_row = from_row + step_row
            cur_col = from_col + step_col

            # Walk diagonally until destination 
            while cur_row != to_row or cur_col != to_col:
                middle_square = position_to_square((cur_row, cur_col))

                if self.get_piece(middle_square) is not None:
                    return fail()  # blocked

                cur_row += step_row
                cur_col += step_col

            # Destination cannot capture your own piece
            target_piece = self.get_piece(to_square)
            if target_piece is not None and target_piece.color == piece.color:
                return fail()
            
        # Queen movement blocking  
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
                    return fail()  # blocked

                # Move to next square in the path
                cur_row += step_row
                cur_col += step_col

            # Final square cannot capture your own piece
            target_piece = self.get_piece(to_square)
            if target_piece is not None and target_piece.color == piece.color:
                return fail()

        # King normal move: cannot capture your own piece (castling already handled above)
        if isinstance(piece, King):
            target_piece = self.get_piece(to_square)
            if target_piece is not None and target_piece.color == piece.color:
                return fail()
    
        # # Variables to track a potential en passant capture so we can undo it if the move is illegal     
        captured_en_passant_square = None
        captured_en_passant_piece = None

        # Save what is currently on the destination square 
        captured_piece = self.get_piece(to_square)

        # If this is an en passant capture, remove the pawn behind the target square
        if isinstance(piece, Pawn) and from_col != to_col and captured_piece is None and old_en_passant_target == to_square:
            # Captured pawn is on the same rank the capturing pawn started from
            captured_en_passant_square = position_to_square((from_row, to_col))
            captured_en_passant_piece = self.get_piece(captured_en_passant_square)

            # Must exist and must be opponent pawn
            if (captured_en_passant_piece is None 
                or not isinstance(captured_en_passant_piece, Pawn)
                or captured_en_passant_piece.color == piece.color
            ):
                return fail()

            # Remove it temporarily (like a capture)
            self.set_piece(captured_en_passant_square, None)

        # Make the move temporarily
        self.set_piece(to_square, piece)
        self.set_piece(from_square, None)

        # Illegal if it leaves your king in check
        if self.is_in_check(turn_color):
            # Undo the normal move
            self.set_piece(from_square, piece) 
            self.set_piece(to_square, captured_piece)
            
            # Restore en passant captured pawn if we removed one
            if captured_en_passant_square is not None:
                self.set_piece(captured_en_passant_square, captured_en_passant_piece)
            
            return fail()

        piece.has_moved = True # Mark piece as having moved

        # Get the piece that just moved to the destination square
        moved_piece = self.get_piece(to_square)

        if isinstance(moved_piece, Pawn): # Check if the moved piece is a Pawn
            # If a WHITE pawn reaches rank 8 → promote to Queen
            if moved_piece.color == WHITE and to_square[1] == "8":
                self.set_piece(to_square, Queen(WHITE))

            # If a BLACK pawn reaches rank 1 → promote to Queen
            elif moved_piece.color == BLACK and to_square[1] == "1":
                self.set_piece(to_square, Queen(BLACK))

        return True # Move completed successfully