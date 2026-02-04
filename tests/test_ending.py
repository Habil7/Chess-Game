from chessgame.board import Board
from chessgame.pieces import King, Queen, Rook, WHITE, BLACK

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

# Test that it is not checkmate if the king can capture the attacking piece
def test_not_checkmate_if_king_can_capture_attacker():
    b = Board()

    # Black king in check by a rook right next to it
    b.set_piece("e8", King(BLACK))
    b.set_piece("e7", Rook(WHITE))

    # White king placed far away 
    b.set_piece("a1", King(WHITE))

    assert b.is_in_check(BLACK) is True

    # Not checkmate because black king can capture the rook on e7
    assert b.is_checkmate(BLACK) is False
    assert b.has_any_legal_move(BLACK) is True

# Test that it is not checkmate if the check can be blocked by another piece
def test_not_checkmate_if_check_can_be_blocked():
    b = Board()
    b.set_piece("e1", Rook(WHITE))
    b.set_piece("e8", King(BLACK))

    # Black queen can block by moving to e7
    b.set_piece("d7", Queen(BLACK))

    # White king far away (legal position)
    b.set_piece("a1", King(WHITE))

    assert b.is_in_check(BLACK) is True

    # Not checkmate because black can play Qe7 to block
    assert b.is_checkmate(BLACK) is False
    assert b.has_any_legal_move(BLACK) is True

# Test that it is not checkmate if another piece can capture the attacker
def test_not_checkmate_if_attacker_can_be_captured_by_piece():
    b = Board()

    # Black king in check from a white rook
    b.set_piece("e8", King(BLACK))
    b.set_piece("e7", Rook(WHITE))

    # Black queen can capture the checking rook 
    b.set_piece("d7", Queen(BLACK))

    # White king far away so position is legal
    b.set_piece("a1", King(WHITE))

    assert b.is_in_check(BLACK) is True

    # Not checkmate because black can capture the attacker with the queen
    assert b.is_checkmate(BLACK) is False
    assert b.has_any_legal_move(BLACK) is True