from chessgame.board import Board
from chessgame.pieces import Pawn, WHITE, BLACK
from chessgame.save_load import save_game, load_game

# Test saving and loading a game state
def test_save_and_load(tmp_path, monkeypatch):
    # Redirect saves folder into pytest temp folder
    monkeypatch.setattr("chessgame.save_load.SAVES_DIR", tmp_path)

    b = Board()
    b.set_piece("e2", Pawn(WHITE))
    turn = BLACK

    save_game(b, turn, "test1")

    b2 = Board()
    loaded_turn = load_game(b2, "test1")

    assert loaded_turn == BLACK
    assert b2.get_piece("e2") is not None
    assert b2.get_piece("e2").color == WHITE