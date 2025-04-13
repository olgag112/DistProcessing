import pygame
from Piece import Piece

#pygame.init()                      dynamicnze dostosowywanie planszy ale cos nie dziala
#info = pygame.display.Info()
#WIDTH, HEIGHT = info.current_w, info.current_h
#WIDTH = min(WIDTH, 800)
#HEIGHT = min(HEIGHT, 800)

WIDTH, HEIGHT = 800, 700        # śmialo zmieniac jesli macie za duza plansze
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Warcaby")

board = [[None for _ in range(COLS)] for _ in range(ROWS)]

def draw_board(win):
    win.fill(BLACK)
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(win, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def create_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 != 0:  # Tylko ciemne pola
                if row < 3:
                    # Czerwone pionki w 1-2 rzędzie
                    king = (row == 2 and col % 2 == 0)  # W 2. rzędzie pionki co drugi będą damkami
                    board[row][col] = Piece(row, col, RED, king)
                elif row >= 4:
                    # Białe pionki w 5-6 rzędzie
                    king = (row == 5 and col % 2 == 1)  # W 6. rzędzie pionki co drugi będą damkami
                    board[row][col] = Piece(row, col, WHITE, king)



def draw_all(win):
    draw_board(win)
    for row in board:
        for piece in row:
            if piece:
                piece.draw(win)
    pygame.display.update()

def get_square(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def is_valid_move(piece, new_row, new_col):
    if not (0 <= new_row < ROWS and 0 <= new_col < COLS):
        return False
    if board[new_row][new_col] is not None:
        return False

    dx = new_col - piece.col
    dy = new_row - piece.row

    if abs(dx) != 1:
        return False

    if piece.king:
        return abs(dy) == 1
    elif piece.color == RED:
        return dy == 1
    else:
        return dy == -1


def move(piece, row, col):
    board[piece.row][piece.col] = None
    piece.row = row
    piece.col = col
    piece.calc_pos()

    # Promocja na damkę, jeśli pionek dotarł do ostatniego rzędu
    if piece.color == RED and piece.row == 0:
        piece.make_king()
    elif piece.color == WHITE and piece.row == 7:
        piece.make_king()

    board[row][col] = piece


def main():
    clock = pygame.time.Clock()
    run = True
    selected_piece = None

    create_pieces()

    while run:
        clock.tick(60)
        draw_all(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_square(pygame.mouse.get_pos())

                if selected_piece:
                    if is_valid_move(selected_piece, row, col):
                        move(selected_piece, row, col)
                    selected_piece = None
                else:
                    piece = board[row][col]
                    if piece:
                        selected_piece = piece

    pygame.quit()

if __name__ == "__main__":
    main()