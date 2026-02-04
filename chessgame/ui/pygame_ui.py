import pygame

SQUARE_SIZE = 80
BOARD_SIZE = 8
WINDOW_SIZE = SQUARE_SIZE * BOARD_SIZE

LIGHT = (238, 238, 210)
DARK  = (118, 150, 86)
SELECT = (246, 246, 105)   # highlight selected

def square_from_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

def draw_board(screen, selected=None):
    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

    if selected is not None:
        row, col = selected
        rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, SELECT, rect, 4)
