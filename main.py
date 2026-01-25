from chessgame.board import Board

def main():
    print("Chess Game and First Project started and launched!")

    board = Board()
    board.setup_starting_position()
    board.print_board()


if __name__ == "__main__":
    main()