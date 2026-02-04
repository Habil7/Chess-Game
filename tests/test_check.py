from chessgame.board import Board
from chessgame.pieces import King, Rook, WHITE, BLACK

# Test that the board correctly detects when the white king is in check
def test_king_in_check_detected():
    b = Board()
    b.set_piece("e1", King(WHITE))
    b.set_piece("e8", King(BLACK))
    b.set_piece("e5", Rook(BLACK))

    assert b.is_in_check(WHITE) is True

# Test that a king cannot move into a square that is under attack
def test_cannot_move_into_check():
    b = Board()
    b.set_piece("e1", King(WHITE))
    b.set_piece("e8", King(BLACK))
    b.set_piece("e5", Rook(BLACK))

    # Moving king into rook line should be illegal!!
    moved = b.move_piece("e1", "e2", WHITE)
    assert moved is False

# Test that kings cannot move to squares next to each other
def test_king_cannot_move_next_to_enemy_king():
    b = Board()
    b.set_piece("e4", King(WHITE))
    b.set_piece("e6", King(BLACK))

    # White king tries to move next to black king
    assert b.move_piece("e4", "e5", WHITE) is False