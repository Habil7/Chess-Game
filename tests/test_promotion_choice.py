from chessgame.board import Board
from chessgame.pieces import Pawn, Queen, Rook, Knight, WHITE, BLACK

# Test that a white pawn can promote to a knight
def test_white_pawn_promotion_to_knight():
    b = Board()
    b.set_piece("a7", Pawn(WHITE))

    assert b.move_piece("a7", "a8", WHITE) is True
    assert b.promote_pawn("a8", "N") is True

    p = b.get_piece("a8")
    assert isinstance(p, Knight)
    assert p.color == WHITE

# Test that a black pawn can promote to a rook
def test_black_pawn_promotion_to_rook():
    b = Board()
    b.set_piece("h2", Pawn(BLACK))

    assert b.move_piece("h2", "h1", BLACK) is True
    assert b.promote_pawn("h1", "R") is True

    p = b.get_piece("h1")
    assert isinstance(p, Rook)
    assert p.color == BLACK

# Test that an invalid promotion choice defaults to a queen
def test_invalid_choice_defaults_to_queen():
    b = Board()
    b.set_piece("b7", Pawn(WHITE))

    assert b.move_piece("b7", "b8", WHITE) is True
    assert b.promote_pawn("b8", "X") is True # invalid => Queen

    p = b.get_piece("b8")
    assert isinstance(p, Queen)
    assert p.color == WHITE