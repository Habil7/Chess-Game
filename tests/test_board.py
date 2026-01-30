from chessgame.board import Board
from chessgame.pieces import Pawn, Rook, Knight, Bishop, Queen, King, WHITE, BLACK

# Basic tests for Board class functionality
def test_board_set_and_get_piece_object():
    b = Board()

    b.set_piece("e2", Pawn(WHITE))

    piece = b.get_piece("e2")
    assert isinstance(piece, Pawn)
    assert piece.color == WHITE

    assert b.get_piece("e3") is None

# Test printing the board 
def test_print_board_runs(capsys):
    b = Board()
    b.print_board()
    out = capsys.readouterr().out
    assert "a b c d e f g h" in out

# Test setting up the standard starting position
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

# Test moving pieces
def test_move_piece_success():
    b = Board()
    b.setup_starting_position()

    moved = b.move_piece("e2", "e4", WHITE)
    assert moved is True

    assert b.get_piece("e2") is None
    assert isinstance(b.get_piece("e4"), Pawn)
    assert b.get_piece("e4").color == WHITE

# Test moving from an empty square fails
def test_move_piece_fail_empty_square():
    b = Board()

    moved = b.move_piece("e3", "e4", WHITE)
    assert moved is False

# Test moving opponent's piece fails
def test_cannot_move_opponent_piece():
    b = Board()
    b.setup_starting_position()

    moved = b.move_piece("e7", "e5", WHITE)  
    assert moved is False

    # Board should be unchanged
    assert b.get_piece("e7") is not None
    assert b.get_piece("e5") is None

# Pawn movement tests
def test_pawn_legal_one_step_forward():
    b = Board()
    b.setup_starting_position()

    moved = b.move_piece("e2", "e3", WHITE)
    assert moved is True

# Pawn two-step from starting position
def test_pawn_illegal_backward_move():
    b = Board()
    b.setup_starting_position()

    moved = b.move_piece("e2", "e3", WHITE)
    assert moved is True

    moved_back = b.move_piece("e3", "e2", WHITE)
    assert moved_back is False

# Pawn two-step from starting position 
def test_pawn_cannot_move_forward_into_piece():
    b = Board()
    b.set_piece("e2", Pawn(WHITE))
    b.set_piece("e3", Pawn(BLACK))

    moved = b.move_piece("e2", "e3", WHITE)
    assert moved is False

# Pawn two-step from starting position
def test_pawn_two_step_cannot_jump_over_piece():
    b = Board()
    b.set_piece("e2", Pawn(WHITE))
    b.set_piece("e3", Pawn(BLACK))

    moved = b.move_piece("e2", "e4", WHITE)
    assert moved is False

# Pawn diagonal capture requires opponent piece
def test_pawn_diagonal_capture_requires_opponent():
    b = Board()
    b.set_piece("e2", Pawn(WHITE))

    # diagonal to empty square should fail
    moved = b.move_piece("e2", "f3", WHITE)
    assert moved is False

# Pawn diagonal capture works
def test_pawn_diagonal_capture_works():
    b = Board()
    b.set_piece("e2", Pawn(WHITE))
    b.set_piece("f3", Pawn(BLACK))

    moved = b.move_piece("e2", "f3", WHITE)
    assert moved is True
    assert b.get_piece("e2") is None
    assert isinstance(b.get_piece("f3"), Pawn)
    assert b.get_piece("f3").color == WHITE

# Rook movement tests
def test_rook_straight_move_works():
    b = Board()
    b.set_piece("a1", Rook(WHITE))

    moved = b.move_piece("a1", "a4", WHITE)
    assert moved is True
    assert b.get_piece("a1") is None
    assert b.get_piece("a4").__class__.__name__ == "Rook"

# Rook cannot move diagonally
def test_rook_cannot_move_diagonal():
    b = Board()
    b.set_piece("a1", Rook(WHITE))

    moved = b.move_piece("a1", "b2", WHITE)
    assert moved is False

# Rook cannot jump over pieces
def test_rook_cannot_jump_over_piece():
    b = Board()
    b.set_piece("a1", Rook(WHITE))
    b.set_piece("a2", Pawn(WHITE)) # blocker

    moved = b.move_piece("a1", "a4", WHITE)
    assert moved is False

# Rook capturing tests
def test_rook_can_capture_opponent():
    b = Board()
    b.set_piece("a1", Rook(WHITE))
    b.set_piece("a4", Pawn(BLACK))

    moved = b.move_piece("a1", "a4", WHITE)
    assert moved is True
    assert b.get_piece("a4").__class__.__name__ == "Rook"
    assert b.get_piece("a4").color == WHITE

# Rook cannot capture own piece
def test_rook_cannot_capture_own_piece():
    b = Board()
    b.set_piece("a1", Rook(WHITE))
    b.set_piece("a4", Pawn(WHITE))

    moved = b.move_piece("a1", "a4", WHITE)
    assert moved is False

# Bishop movement tests
def test_bishop_diagonal_move_works():
    b = Board()
    b.set_piece("c1", Bishop(WHITE))

    moved = b.move_piece("c1", "f4", WHITE)
    assert moved is True
    assert b.get_piece("c1") is None
    assert b.get_piece("f4").__class__.__name__ == "Bishop"

# Bishop cannot move straight
def test_bishop_cannot_move_straight():
    b = Board()
    b.set_piece("c1", Bishop(WHITE))

    moved = b.move_piece("c1", "c3", WHITE)
    assert moved is False

# Bishop cannot jump over pieces
def test_bishop_cannot_jump_over_piece():
    b = Board()
    b.set_piece("c1", Bishop(WHITE))
    b.set_piece("d2", Pawn(WHITE))  # blocker

    moved = b.move_piece("c1", "f4", WHITE)
    assert moved is False

# Bishop capturing tests
def test_bishop_can_capture_opponent():
    b = Board()
    b.set_piece("c1", Bishop(WHITE))
    b.set_piece("f4", Pawn(BLACK))

    moved = b.move_piece("c1", "f4", WHITE)
    assert moved is True
    assert b.get_piece("f4").__class__.__name__ == "Bishop"
    assert b.get_piece("f4").color == WHITE

# Bishop cannot capture own piece
def test_bishop_cannot_capture_own_piece():
    b = Board()
    b.set_piece("c1", Bishop(WHITE))
    b.set_piece("f4", Pawn(WHITE))

    moved = b.move_piece("c1", "f4", WHITE)
    assert moved is False

# Knight movement tests
def test_knight_l_move_works():
    b = Board()
    b.set_piece("b1", Knight(WHITE))

    moved = b.move_piece("b1", "a3", WHITE)
    assert moved is True
    assert b.get_piece("b1") is None
    assert b.get_piece("a3").__class__.__name__ == "Knight"

# Knight cannot move like bishop or rook
def test_knight_cannot_move_like_bishop_or_rook():
    b = Board()
    b.set_piece("b1", Knight(WHITE))

    moved1 = b.move_piece("b1", "b3", WHITE)  # straight
    moved2 = b.move_piece("b1", "c2", WHITE)  # diagonal-ish
    assert moved1 is False
    assert moved2 is False

# Knight can jump over pieces
def test_knight_can_jump_over_pieces():
    b = Board()
    b.set_piece("b1", Knight(WHITE))
    b.set_piece("b2", Pawn(WHITE))  # blocker doesn't matter

    moved = b.move_piece("b1", "a3", WHITE)
    assert moved is True

# Knight capturing tests
def test_knight_can_capture_opponent():
    b = Board()
    b.set_piece("b1", Knight(WHITE))
    b.set_piece("a3", Pawn(BLACK))

    moved = b.move_piece("b1", "a3", WHITE)
    assert moved is True
    assert b.get_piece("a3").__class__.__name__ == "Knight"
    assert b.get_piece("a3").color == WHITE

# Knight cannot capture own piece
def test_knight_cannot_capture_own_piece():
    b = Board()
    b.set_piece("b1", Knight(WHITE))
    b.set_piece("a3", Pawn(WHITE))

    moved = b.move_piece("b1", "a3", WHITE)
    assert moved is False

# Queen movement tests
def test_queen_rook_like_move_works():
    b = Board()
    b.set_piece("d4", Queen(WHITE))

    moved = b.move_piece("d4", "d7", WHITE)
    assert moved is True
    assert b.get_piece("d4") is None
    assert isinstance(b.get_piece("d7"), Queen)

# Queen movement tests
def test_queen_bishop_like_move_works():
    b = Board()
    b.set_piece("d4", Queen(WHITE))

    moved = b.move_piece("d4", "g7", WHITE)
    assert moved is True
    assert b.get_piece("d4") is None
    assert isinstance(b.get_piece("g7"), Queen)

# Queen cannot move like knight
def test_queen_cannot_move_like_knight():
    b = Board()
    b.set_piece("d4", Queen(WHITE))

    moved = b.move_piece("d4", "e6", WHITE)
    assert moved is False

# Queen cannot jump over pieces
def test_queen_cannot_jump_over_piece():
    b = Board()
    b.set_piece("d4", Queen(WHITE))
    b.set_piece("d6", Pawn(WHITE)) # blocker

    moved = b.move_piece("d4", "d7", WHITE)
    assert moved is False

# Queen capturing tests
def test_queen_can_capture_opponent():
    b = Board()
    b.set_piece("d4", Queen(WHITE))
    b.set_piece("d7", Pawn(BLACK))

    moved = b.move_piece("d4", "d7", WHITE)
    assert moved is True
    assert isinstance(b.get_piece("d7"), Queen)
    assert b.get_piece("d7").color == WHITE

# Queen cannot capture own piece
def test_queen_cannot_capture_own_piece():
    b = Board()
    b.set_piece("d4", Queen(WHITE))
    b.set_piece("d7", Pawn(WHITE))

    moved = b.move_piece("d4", "d7", WHITE)
    assert moved is False

# King movement tests
def test_king_one_step_move_works():
    b = Board()
    b.set_piece("e4", King(WHITE))

    moved = b.move_piece("e4", "e5", WHITE)
    assert moved is True
    assert b.get_piece("e4") is None
    assert isinstance(b.get_piece("e5"), King)

# King diagonal move
def test_king_diagonal_move_works():
    b = Board()
    b.set_piece("e4", King(WHITE))

    moved = b.move_piece("e4", "f5", WHITE)
    assert moved is True

# King cannot move two squares
def test_king_cannot_move_two_squares():
    b = Board()
    b.set_piece("e4", King(WHITE))

    moved1 = b.move_piece("e4", "e6", WHITE)
    assert moved1 is False

    moved2 = b.move_piece("e4", "g4", WHITE)
    assert moved2 is False

# King capturing tests
def test_king_can_capture_opponent():
    b = Board()
    b.set_piece("e4", King(WHITE))
    b.set_piece("f5", Pawn(BLACK))

    moved = b.move_piece("e4", "f5", WHITE)
    assert moved is True
    assert isinstance(b.get_piece("f5"), King)
    assert b.get_piece("f5").color == WHITE

# King cannot capture own piece
def test_king_cannot_capture_own_piece():
    b = Board()
    b.set_piece("e4", King(WHITE))
    b.set_piece("f5", Pawn(WHITE))

    moved = b.move_piece("e4", "f5", WHITE)
    assert moved is False

# Test try_move_no_turn_switch
def test_try_move_no_turn_switch_does_not_change_board():
    b = Board()
    b.setup_starting_position()

    before_from = b.get_piece("e2")
    before_to = b.get_piece("e4")

    result = b.try_move_no_turn_switch("e2", "e4", WHITE)
    assert result is True

    # Board must be unchanged
    assert b.get_piece("e2") is before_from
    assert b.get_piece("e4") is before_to
