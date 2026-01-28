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