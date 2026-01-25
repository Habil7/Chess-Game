from chessgame.board import Board

def test_board_set_and_get_piece():
    b = Board()

    b.set_piece("e2", "P")

    assert b.get_piece("e2") == "P"
    assert b.get_piece("e3") is None


def test_print_board_runs(capsys):
    b = Board()
    b.print_board()
    out = capsys.readouterr().out
    assert "a b c d e f g h" in out