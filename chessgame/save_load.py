import json
from pathlib import Path # We import Path for file path manipulations
from chessgame.pieces import Pawn, Rook, Knight, Bishop, Queen, King

SAVES_DIR = Path("saves") # Directory to store save files

def piece_to_record(square: str, piece: object) -> dict:
    """Convert a chess piece to a serializable record.
    """
    return {
        "square": square,                 # Position on the board (e.g., 'e4')
        "type": piece.__class__.__name__, # Type of the piece (e.g., Pawn, Rook)
        "color": piece.color,             # White or Black
    }

def record_to_piece(type_name: str, color: str) -> object:
    """Convert a record back to a chess piece object.
    """
    if type_name == "Pawn":
        return Pawn(color)
    if type_name == "Rook":
        return Rook(color)
    if type_name == "Knight":
        return Knight(color)
    if type_name == "Bishop":
        return Bishop(color)
    if type_name == "Queen":
        return Queen(color)
    if type_name == "King":
        return King(color)
    
    raise ValueError(f"Unknown piece type: {type_name}")

def save_game(board, turn: str, save_name: str) -> None:
    """Save the current game state to a file.
    """
    SAVES_DIR.mkdir(exist_ok = True) # Ensure the saves directory exists
    
    data = {"turn": turn, "pieces": []}
    
    from chessgame.types import position_to_square

    # It helps to convert board positions to square notation
    for row in range(8):
        for col in range(8):
            piece = board.grid[row][col]
            if piece is None:
                continue

            square = position_to_square((row, col))
            data["pieces"].append(piece_to_record(square, piece))

    path = SAVES_DIR / f"{save_name}.json" # Save file path
    path.write_text(json.dumps(data, indent = 2), encoding = "utf-8")

def list_saves() -> list[str]:
    """List all saved games.
    """
    if not SAVES_DIR.exists():
        return []
    return sorted(p.stem for p in SAVES_DIR.glob("*.json"))

def load_game(board, save_name: str) -> str:
    """Load a saved game state from a file.
    """
    path = SAVES_DIR / f"{save_name}.json"
    data = json.loads(path.read_text(encoding = "utf-8"))
    
    # Clear the board first
    for row in range(8):
        for col in range(8):
            board.grid[row][col] = None

    # Restore pieces
    for rec in data["pieces"]:
        piece = record_to_piece(rec["type"], rec["color"])
        board.set_piece(rec["square"], piece)

    return data["turn"] # White or Black