from chessgame.board import Board

def main():
    """Main function to start the chess game.
    """
    print("Chess Game and First Project started and launched!")

    board = Board()
    board.setup_starting_position()
    board.print_board()

    while True:
        move = input("Enter your move (e.g., e2 e4) or 'quit' to exit: ").strip()

        if move == "quit" or move == "exit":
            print("Exiting the game.")
            break

        parts = move.split()

        if len(parts) != 2:
            print("Invalid move format. Please enter moves like 'e2 e4'.")
            continue

        from_square, to_square = parts

        move_successful = board.move_piece(from_square, to_square)

        if not move_successful:
            print("Invalid move. No piece on that square. Please try again.")
            continue
        
        board.print_board()

if __name__ == "__main__":
    main()