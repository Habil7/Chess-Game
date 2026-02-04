from chessgame.board import Board
from chessgame.pieces import Pawn, King, Rook, WHITE, BLACK
from chessgame.save_load import save_game, load_game

# Test saving and loading a game state
def test_save_and_load(tmp_path, monkeypatch):
    # Redirect saves folder into pytest temp folder
    monkeypatch.setattr("chessgame.save_load.SAVES_DIR", tmp_path)

    # Create a new board
    b = Board()

    # Create a white pawn and mark it as moved
    pawn = Pawn(WHITE)
    pawn.has_moved = True
    b.set_piece("e2", pawn)

    # Set en passant target
    b.en_passant_target = "d6"

    # Create a black king and mark it as moved
    king = King(BLACK)
    king.has_moved = True
    b.set_piece("e8", king)

    # Set current turn
    turn = BLACK

    save_game(b, turn, "test1")

    # Load the game into a new board
    b2 = Board()
    loaded_turn = load_game(b2, "test1")

    # Check turn is loaded correctly
    assert loaded_turn == BLACK

    # Check pawn exists and has correct color
    assert b2.get_piece("e2") is not None
    assert b2.get_piece("e2").color == WHITE

    # Check moved flags and en passant target
    assert b2.get_piece("e2").has_moved is True
    assert b2.get_piece("e8").has_moved is True
    assert b2.en_passant_target == "d6"

def test_save_load_preserves_castling_rights(tmp_path, monkeypatch):
    # A temporary folder and lets you temporarily change varuables  or functions
    # during the test
    monkeypatch.setattr("chessgame.save_load.SAVES_DIR", tmp_path)

    # Create board
    b = Board()

    # Create king and rook
    k = King(WHITE)
    r = Rook(WHITE)

    # King already moved so castling should be illegal
    k.has_moved = True

    b.set_piece("e1", k)
    b.set_piece("h1", r)

    # Save game
    save_game(b, WHITE, "castle_state")

    # Load game
    b2 = Board()
    load_game(b2, "castle_state")

    # Castling must still be illegal after load
    assert b2.move_piece("e1", "g1", WHITE) is False