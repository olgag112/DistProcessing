import pygame

SQUARE_SIZE = 800 // 8
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load("crown.png"), (44, 25))

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color, king=False):
        self.row = row
        self.col = col
        self.color = color
        self.king = king
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
        print(f"Pionek na pozycji ({self.row}, {self.col}) stał się damką!")

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))
