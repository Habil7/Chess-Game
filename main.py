from chessgame.board import Board
from chessgame.pieces import WHITE, BLACK

def is_valid_square(square: str) -> bool:
    """Check if the given square (e.g., 'e4') is a valid chess board square.
    """
    if len(square) != 2:
        return False
    
    file = square[0]
    rank = square[1]

    if file < 'a' or file > 'h':
        return False
    
    if rank < '1' or rank > '8':
        return False
    
    return True


def main():
    """Main function to start the chess game.
    """
    print("Chess Game and First Project started and launched!")

    board = Board()
    board.setup_starting_position()
    board.print_board()

    turn = WHITE  # White starts first, always

    while True:
        print(f"\nTurn: {turn}")
        move = input("Enter your move (e.g., e2 e4) or 'quit' to exit: ").strip()

        if move == "quit" or move == "exit":
            print("Exiting the game.")
            break

        parts = move.split()

        if len(parts) != 2:
            print("Invalid move format. Please enter moves like 'e2 e4'.")
            continue

        from_square, to_square = parts

        if not is_valid_square(from_square) or not is_valid_square(to_square):
            print("Invalid square. Please use squares like e2 e4.")
            continue

        move_successful = board.move_piece(from_square, to_square, turn)

        if not move_successful:
            print("Invalid move. Please try again.")
            continue

        board.print_board() # Print the board after the move

        # Check for checkmate or stalemate
        opponent = BLACK if turn == WHITE else WHITE

        # Check for check
        if board.is_in_check(opponent):
            print(f"CHECK! {opponent} is in check!") # Notify if the current player is in check

        # Check for checkmate
        if board.is_checkmate(opponent):
            print(f"CHECKMATE! {turn} wins!")
            break

        # Check for stalemate
        if board.is_stalemate(opponent):
            print("STALEMATE! The game is a draw.")
            break

        # Switch the turn
        turn = opponent

if __name__ == "__main__":
    main()