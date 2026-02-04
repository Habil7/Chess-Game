# Chess Game (Project ASTRA)

This project is a fully playable **two-player command-line chess game** written in Python. It was developed as an academic project with a focus on **object-oriented design**, **rule correctness**, **state management**, and **unit testing**.

---

## Features

- Two-player chess playable on the same machine
- Command-line chessboard display
- Legal move enforcement for all pieces
- Detection of **check**, **checkmate**, and **stalemate**
- Full support for special moves:
  - Castling
  - En passant
  - Pawn promotion with **user-selected piece** (Q/R/B/N)
- Save and load games with custom names
- Multiple saved games selectable at startup
- Comprehensive unit test suite (60+ tests)

---

## Project Structure

```
chessgame/
├── board.py                   # Core game logic and rule enforcement
├── pieces.py                  # Chess piece definitions and movement rules
├── save_load.py               # Save/load functionality using JSON
├── types.py                   # Board coordinate helpers
├── main.py                    # Command-line interface (game loop)

tests/
├── test_board.py             # Board state and move validation tests
├── test_check.py             # Check detection tests
├── test_ending.py            # Checkmate and stalemate tests
├── test_save_load.py         # Persistence tests
├── test_promotion_choice.py  # Pawn promotion tests
└── test_sanity.py            # Basic sanity checks
```

---
## How to Run Tests

This project uses pytest for unit testing.

```bash
pytest -q
```

All tests should pass.

---

## Design Notes

- The game logic is separated from the command-line interface to keep the code clean and modular.
- Pawn promotion is handled at the interface level, so the core game logic remains simple and predictable.
- Saving and loading a game preserves all important rule-related state, such as castling and en passant.
- Unit tests are used to verify correctness and prevent regressions as the project evolves.
- The code is structured to allow future extensions, and I plan to continue developing this project by adding a graphical user interface, online play, and additional features.

---
License - This project is licensed under the MIT License.
---
