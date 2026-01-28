from chessgame.board import Board
from chessgame.pieces import WHITE, BLACK, King, Queen

# Test cases for checkmate and stalemate scenarios
def test_checkmate_basic_queen_mate():
    b = Board()

    b.set_piece("a8", King(BLACK))
    b.set_piece("c6", King(WHITE))
    b.set_piece("b7", Queen(WHITE))

    assert b.is_in_check(BLACK) is True
    assert b.is_checkmate(BLACK) is True

# Test stalemate scenario
def test_stalemate_basic():
    b = Board()

    b.set_piece("a8", King(BLACK))
    b.set_piece("c6", King(WHITE))
    b.set_piece("b6", Queen(WHITE))

    assert b.is_in_check(BLACK) is False
    assert b.is_stalemate(BLACK) is True