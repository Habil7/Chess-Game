# In chess vertical columns are called "Files" and horizontal rows are called "Ranks"
FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]

def square_to_position(square: str) -> tuple[int, int]:
    """Converts a chess square into a position on the board grid.
    """
    square = square.strip().lower() # Clean up the input

    # Make sure the input is valid
    if len(square) != 2:
        raise ValueError("Invalid square format. Must be like 'e4'.")
    
    file = square[0] # Split the square into file 
    rank = square[1] # and rank

    # Check if file and rank are valid
    if file < "a" or file > "h":
        raise ValueError("Invalid file. Must be between 'a' and 'h'.")

    if rank < "1" or rank > "8":
        raise ValueError("Invalid rank. Must be between '1' and '8'.")

    # Convert chess coordinates 
    #
    # FILES and RANKS to array ROW and COLUMN indices:
    # columns -> a b  c  d  e  f  g  h
    # files   -> 0 1  2  3  4  5  6  7

    # Rank-to-row conversion: 
    # ranks -> 8  7  6  5  4  3  2  1
    # rows  -> 0  1  2  3  4  5  6  7

    # Why we do that? 
    # - Because arrays start at row 0 from the TOP, but chess ranks start at 8 from the TOP.

    col = FILES.index(file) # Convert file letter to column index
    row = 8 - int(rank)     # Convert rank to row index

    return (row, col)

def position_to_square(position: tuple[int, int]) -> str:
    """Converts a position on the board grid into a chess square.
    """
    # Make sure the input is valid
    if len(position) != 2:
        raise ValueError("Position must be a tuple like (row, col).")
    
    row, col = position

    # Validate the position
    if row < 0 or row > 7:
        raise ValueError("Invalid row index. Must be between 0 and 7.")
    
    if col < 0 or col > 7:
        raise ValueError("Invalid column index. Must be between 0 and 7.")

    file = FILES[col]       # Convert column index to file letter
    rank = str(8 - row)     # Convert row index to rank

    return file + rank