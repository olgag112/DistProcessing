import pygame, sys
from pygame.locals import *

#Colors
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
HIGH     = (160, 190, 255)

class Graphics:
	def __init__(self):
		self.caption = "Checkers"

		self.fps = 60
		self.clock = pygame.time.Clock()

		self.window_size = 600
		self.screen = pygame.display.set_mode((self.window_size, self.window_size))
		self.background = pygame.image.load('resources/board2.png')
		self.king_black = pygame.image.load("resources/king_black.png").convert_alpha()
		self.king_white = pygame.image.load("resources/king_white.png").convert_alpha()

		self.square_size = self.window_size >> 3
		self.piece_size = self.square_size >> 1

		self.message = False

	# Update the window title
	def set_caption(self, caption):
		self.caption = caption
		pygame.display.set_caption(caption)

    # initializing window
	def setup_window(self):
		pygame.init()
		pygame.mixer.init()
		pygame.display.set_caption(self.caption)

		self.move_sound = pygame.mixer.Sound("resources/move_sound.wav")

    # updating the visuals of the board
	def update_display(self, board, legal_moves, selected_piece):
		self.screen.blit(self.background, (0,0))
		
		self.highlight_squares(legal_moves, selected_piece)
		self.draw_board_pieces(board)
		if self.message:
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)

		pygame.display.update()
		self.clock.tick(self.fps)

    # Drawing squares (place where the piece can be put)
	def draw_board_squares(self, board):
		for x in range(8):
			for y in range(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )
	
    # Drawing pieces on the board (normal ones and kings)
	def draw_board_pieces(self, board):
		for x in range(8):
			for y in range(8):
				if board.matrix[x][y].occupant != None:
					pygame.draw.circle(self.screen, BLACK, self.pixel_coords((x,y)), self.piece_size / 1.05) 
					pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, self.pixel_coords((x,y)), self.piece_size / 1.1) 

					if board.location((x,y)).occupant.king == True:
						if board.matrix[x][y].occupant.color == WHITE:
							self.screen.blit(self.king_black, self.king_black.get_rect(center=self.pixel_coords((x,y))))
						else:
							self.screen.blit(self.king_white, self.king_white.get_rect(center=self.pixel_coords((x,y))))


    # center pixel of board's squares
	def pixel_coords(self, board_coords):
		return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

    # convert pixel coord, to square coords (we know on which square we click)
	def board_coords(self, pixel):
		return (pixel[0] // self.square_size, pixel[1] // self.square_size)

    # highliting the squares (board)
	def highlight_squares(self, squares, origin):
		for square in squares:
			pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))	

		if origin != None:
			pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

    
    # Draws message to the screen. 
	def draw_message(self, message):
		self.message = True
		self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (self.window_size >> 1, self.window_size >> 1)
