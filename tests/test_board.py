from chessgame.board import Board
from chessgame.pieces import Pawn, Rook, Knight, Bishop, Queen, King, WHITE, BLACK

def test_board_set_and_get_piece_object():
    b = Board()

    b.set_piece("e2", Pawn(WHITE))

    piece = b.get_piece("e2")
    assert isinstance(piece, Pawn)
    assert piece.color == WHITE

    assert b.get_piece("e3") is None

def test_print_board_runs(capsys):
    b = Board()
    b.print_board()
    out = capsys.readouterr().out
    assert "a b c d e f g h" in out

def test_starting_position_all_pieces():
    b = Board()
    b.setup_starting_position()

    # White back rank
    assert isinstance(b.get_piece("a1"), Rook)
    assert isinstance(b.get_piece("b1"), Knight)
    assert isinstance(b.get_piece("c1"), Bishop)
    assert isinstance(b.get_piece("d1"), Queen)
    assert isinstance(b.get_piece("e1"), King)
    assert isinstance(b.get_piece("f1"), Bishop)
    assert isinstance(b.get_piece("g1"), Knight)
    assert isinstance(b.get_piece("h1"), Rook)

    # Black back rank
    assert isinstance(b.get_piece("a8"), Rook)
    assert isinstance(b.get_piece("b8"), Knight)
    assert isinstance(b.get_piece("c8"), Bishop)
    assert isinstance(b.get_piece("d8"), Queen)
    assert isinstance(b.get_piece("e8"), King)
    assert isinstance(b.get_piece("f8"), Bishop)
    assert isinstance(b.get_piece("g8"), Knight)
    assert isinstance(b.get_piece("h8"), Rook)

    # Pawns (check a few + loop)
    for file in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        assert isinstance(b.get_piece(file + "2"), Pawn)
        assert b.get_piece(file + "2").color == WHITE

        assert isinstance(b.get_piece(file + "7"), Pawn)
        assert b.get_piece(file + "7").color == BLACK

    # Colors on key pieces
    assert b.get_piece("a1").color == WHITE
    assert b.get_piece("e1").color == WHITE
    assert b.get_piece("a8").color == BLACK
    assert b.get_piece("e8").color == BLACK

def test_move_piece_success():
    b = Board()
    b.setup_starting_position()

    moved = b.move_piece("e2", "e4", WHITE)
    assert moved is True

    assert b.get_piece("e2") is None
    assert isinstance(b.get_piece("e4"), Pawn)
    assert b.get_piece("e4").color == WHITE

def test_move_piece_fail_empty_square():
    b = Board()

    moved = b.move_piece("e3", "e4", WHITE)
    assert moved is False

def test_cannot_move_opponent_piece():
    b = Board()
    b.setup_starting_position()

    moved = b.move_piece("e7", "e5", WHITE)  
    assert moved is False

    # Board should be unchanged
    assert b.get_piece("e7") is not None
    assert b.get_piece("e5") is None

def test_pawn_legal_one_step_forward():
    b = Board()
    b.setup_starting_position()

    moved = b.move_piece("e2", "e3", WHITE)
    assert moved is True

def test_pawn_illegal_backward_move():
    b = Board()
    b.setup_starting_position()

    moved = b.move_piece("e2", "e3", WHITE)
    assert moved is True

    moved_back = b.move_piece("e3", "e2", WHITE)
    assert moved_back is False\
    
def test_pawn_cannot_move_forward_into_piece():
    b = Board()
    b.set_piece("e2", Pawn(WHITE))
    b.set_piece("e3", Pawn(BLACK))

    moved = b.move_piece("e2", "e3", WHITE)
    assert moved is False

def test_pawn_two_step_cannot_jump_over_piece():
    b = Board()
    b.set_piece("e2", Pawn(WHITE))
    b.set_piece("e3", Pawn(BLACK))

    moved = b.move_piece("e2", "e4", WHITE)
    assert moved is False

def test_pawn_diagonal_capture_requires_opponent():
    b = Board()
    b.set_piece("e2", Pawn(WHITE))

    # diagonal to empty square should fail
    moved = b.move_piece("e2", "f3", WHITE)
    assert moved is False

def test_pawn_diagonal_capture_works():
    b = Board()
    b.set_piece("e2", Pawn(WHITE))
    b.set_piece("f3", Pawn(BLACK))

    moved = b.move_piece("e2", "f3", WHITE)
    assert moved is True
    assert b.get_piece("e2") is None
    assert isinstance(b.get_piece("f3"), Pawn)
    assert b.get_piece("f3").color == WHITE

def test_rook_straight_move_works():
    b = Board()
    b.set_piece("a1", Rook(WHITE))

    moved = b.move_piece("a1", "a4", WHITE)
    assert moved is True
    assert b.get_piece("a1") is None
    assert b.get_piece("a4").__class__.__name__ == "Rook"

def test_rook_cannot_move_diagonal():
    b = Board()
    b.set_piece("a1", Rook(WHITE))

    moved = b.move_piece("a1", "b2", WHITE)
    assert moved is False

def test_rook_cannot_jump_over_piece():
    b = Board()
    b.set_piece("a1", Rook(WHITE))
    b.set_piece("a2", Pawn(WHITE))  # blocker

    moved = b.move_piece("a1", "a4", WHITE)
    assert moved is False

def test_rook_can_capture_opponent():
    b = Board()
    b.set_piece("a1", Rook(WHITE))
    b.set_piece("a4", Pawn(BLACK))

    moved = b.move_piece("a1", "a4", WHITE)
    assert moved is True
    assert b.get_piece("a4").__class__.__name__ == "Rook"
    assert b.get_piece("a4").color == WHITE

def test_rook_cannot_capture_own_piece():
    b = Board()
    b.set_piece("a1", Rook(WHITE))
    b.set_piece("a4", Pawn(WHITE))

    moved = b.move_piece("a1", "a4", WHITE)
    assert moved is False

def test_bishop_diagonal_move_works():
    b = Board()
    b.set_piece("c1", Bishop(WHITE))

    moved = b.move_piece("c1", "f4", WHITE)
    assert moved is True
    assert b.get_piece("c1") is None
    assert b.get_piece("f4").__class__.__name__ == "Bishop"

def test_bishop_cannot_move_straight():
    b = Board()
    b.set_piece("c1", Bishop(WHITE))

    moved = b.move_piece("c1", "c3", WHITE)
    assert moved is False

def test_bishop_cannot_jump_over_piece():
    b = Board()
    b.set_piece("c1", Bishop(WHITE))
    b.set_piece("d2", Pawn(WHITE))  # blocker

    moved = b.move_piece("c1", "f4", WHITE)
    assert moved is False

def test_bishop_can_capture_opponent():
    b = Board()
    b.set_piece("c1", Bishop(WHITE))
    b.set_piece("f4", Pawn(BLACK))

    moved = b.move_piece("c1", "f4", WHITE)
    assert moved is True
    assert b.get_piece("f4").__class__.__name__ == "Bishop"
    assert b.get_piece("f4").color == WHITE

def test_bishop_cannot_capture_own_piece():
    b = Board()
    b.set_piece("c1", Bishop(WHITE))
    b.set_piece("f4", Pawn(WHITE))

    moved = b.move_piece("c1", "f4", WHITE)
    assert moved is False

def test_knight_l_move_works():
    b = Board()
    b.set_piece("b1", Knight(WHITE))

    moved = b.move_piece("b1", "a3", WHITE)
    assert moved is True
    assert b.get_piece("b1") is None
    assert b.get_piece("a3").__class__.__name__ == "Knight"

def test_knight_cannot_move_like_bishop_or_rook():
    b = Board()
    b.set_piece("b1", Knight(WHITE))

    moved1 = b.move_piece("b1", "b3", WHITE)  # straight
    moved2 = b.move_piece("b1", "c2", WHITE)  # diagonal-ish
    assert moved1 is False
    assert moved2 is False

def test_knight_can_jump_over_pieces():
    b = Board()
    b.set_piece("b1", Knight(WHITE))
    b.set_piece("b2", Pawn(WHITE))  # blocker doesn't matter

    moved = b.move_piece("b1", "a3", WHITE)
    assert moved is True

def test_knight_can_capture_opponent():
    b = Board()
    b.set_piece("b1", Knight(WHITE))
    b.set_piece("a3", Pawn(BLACK))

    moved = b.move_piece("b1", "a3", WHITE)
    assert moved is True
    assert b.get_piece("a3").__class__.__name__ == "Knight"
    assert b.get_piece("a3").color == WHITE

def test_knight_cannot_capture_own_piece():
    b = Board()
    b.set_piece("b1", Knight(WHITE))
    b.set_piece("a3", Pawn(WHITE))

    moved = b.move_piece("b1", "a3", WHITE)
    assert moved is False
    
def test_queen_rook_like_move_works():
    b = Board()
    b.set_piece("d4", Queen(WHITE))

    moved = b.move_piece("d4", "d7", WHITE)
    assert moved is True
    assert b.get_piece("d4") is None
    assert isinstance(b.get_piece("d7"), Queen)

def test_queen_bishop_like_move_works():
    b = Board()
    b.set_piece("d4", Queen(WHITE))

    moved = b.move_piece("d4", "g7", WHITE)
    assert moved is True
    assert b.get_piece("d4") is None
    assert isinstance(b.get_piece("g7"), Queen)

def test_queen_cannot_move_like_knight():
    b = Board()
    b.set_piece("d4", Queen(WHITE))

    moved = b.move_piece("d4", "e6", WHITE)
    assert moved is False

def test_queen_cannot_jump_over_piece():
    b = Board()
    b.set_piece("d4", Queen(WHITE))
    b.set_piece("d6", Pawn(WHITE)) # blocker

    moved = b.move_piece("d4", "d7", WHITE)
    assert moved is False

def test_queen_can_capture_opponent():
    b = Board()
    b.set_piece("d4", Queen(WHITE))
    b.set_piece("d7", Pawn(BLACK))

    moved = b.move_piece("d4", "d7", WHITE)
    assert moved is True
    assert isinstance(b.get_piece("d7"), Queen)
    assert b.get_piece("d7").color == WHITE

def test_queen_cannot_capture_own_piece():
    b = Board()
    b.set_piece("d4", Queen(WHITE))
    b.set_piece("d7", Pawn(WHITE))

    moved = b.move_piece("d4", "d7", WHITE)
    assert moved is False

def test_king_one_step_move_works():
    b = Board()
    b.set_piece("e4", King(WHITE))

    moved = b.move_piece("e4", "e5", WHITE)
    assert moved is True
    assert b.get_piece("e4") is None
    assert isinstance(b.get_piece("e5"), King)

def test_king_diagonal_move_works():
    b = Board()
    b.set_piece("e4", King(WHITE))

    moved = b.move_piece("e4", "f5", WHITE)
    assert moved is True

def test_king_cannot_move_two_squares():
    b = Board()
    b.set_piece("e4", King(WHITE))

    moved1 = b.move_piece("e4", "e6", WHITE)
    assert moved1 is False

    moved2 = b.move_piece("e4", "g4", WHITE)
    assert moved2 is False

def test_king_can_capture_opponent():
    b = Board()
    b.set_piece("e4", King(WHITE))
    b.set_piece("f5", Pawn(BLACK))

    moved = b.move_piece("e4", "f5", WHITE)
    assert moved is True
    assert isinstance(b.get_piece("f5"), King)
    assert b.get_piece("f5").color == WHITE

def test_king_cannot_capture_own_piece():
    b = Board()
    b.set_piece("e4", King(WHITE))
    b.set_piece("f5", Pawn(WHITE))

    moved = b.move_piece("e4", "f5", WHITE)
    assert moved is False