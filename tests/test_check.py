from chessgame.board import Board
from chessgame.pieces import King, Rook, WHITE, BLACK

def test_king_in_check_detected():
    b = Board()
    b.set_piece("e1", King(WHITE))
    b.set_piece("e8", King(BLACK))
    b.set_piece("e5", Rook(BLACK))

    assert b.is_in_check(WHITE) is True

def test_cannot_move_into_check():
    b = Board()
    b.set_piece("e1", King(WHITE))
    b.set_piece("e8", King(BLACK))
    b.set_piece("e5", Rook(BLACK))

    # Moving king into rook line should be illegal
    moved = b.move_piece("e1", "e2", WHITE)
    assert moved is False