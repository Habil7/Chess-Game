from chessgame.board import Board

def main():
    print("Chess Game and First Project started and launched!")

    board = Board()

    # temporary pieces just to visualize
    board.set_piece("e2", "P")
    board.set_piece("e7", "p")

    board.print_board()


if __name__ == "__main__":
    main()
