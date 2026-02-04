from chessgame.board import Board
from chessgame.pieces import WHITE, BLACK
from chessgame.save_load import save_game, load_game, list_saves

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

    board = Board() # Initialize the chess board

    # Offer to load a saved game or start a new one
    print("1) New game")  
    print("2) Load game") 
    choice = input("Select an option (1 or 2): ").strip()

    # Handle loading a saved game
    if choice == "2":
        saves = list_saves()
        if len(saves) == 0:
            print("No saved games found. Starting a new game.")
            board.setup_starting_position()
            turn = WHITE
        else:
            print("Saved games:")
            for i, name in enumerate(saves, start = 1):
                print(f"{i}) {name}")

            pick = input("Select a saved game by number: ").strip()
            if not pick.isdigit():
                print("Invalid selection! Starting a new game.")
                board.setup_starting_position()
                turn = WHITE
            else:
                idx = int(pick) - 1
                if idx < 0 or idx >= len(saves):
                    print("Invalid selection! Starting a new game.")
                    board.setup_starting_position()
                    turn = WHITE
                else:
                    save_name = saves[idx]
                    turn = load_game(board, save_name)

    else:
        board.setup_starting_position()
        turn = WHITE  # White starts first, always

    board.print_board()
  
    while True:
        print(f"\nTurn: {turn}") # Indicate whose turn it is
        move = input("Enter move (e2 e4), 'save NAME', or 'quit': ").strip()

        # Handle quitting the game
        if move == "quit" or move == "exit":
            print("Exiting the game.")
            break

        # Handle saving the game
        if move.lower().startswith("save"):
            parts = move.split()
            if len(parts) != 2:
                print("Use: save NAME")
                continue
            save_name = parts[1]
            save_game(board, turn, save_name)
            print(f"Game saved as '{save_name}'.")
            continue

        parts = move.split()

        if len(parts) != 2:
            print("Invalid move format. Please enter moves like 'e2 e4'.")
            continue

        from_square, to_square = parts

        if not is_valid_square(from_square) or not is_valid_square(to_square):
            print("Invalid square. Please use squares like e2 e4.")
            continue
        
        # Try to move a piece from one square to another
        move_successful = board.move_piece(from_square, to_square, turn)
        
        if not move_successful:
            print("Invalid move. Please try again.")
            continue

        # Pawn promotion choice 
        piece = board.get_piece(to_square)

        # Check that the piece exists and is a pawn
        if piece is not None and piece.__class__.__name__ == "Pawn":
            # Check if the pawn reached the last rank for promotion
            if (piece.color == WHITE and to_square[1] == "8") or (piece.color == BLACK and to_square[1] == "1"):
                # Ask the player what piece to promote to
                choice = input("Promote pawn to (Q/R/B/N): ")
                # Promote the pawn using the Board method
                board.promote_pawn(to_square, choice)

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