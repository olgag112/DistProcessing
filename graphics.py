import pygame, sys
from pygame.locals import *

#Colors
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
HIGH     = (160, 190, 255)

"""
Handles rendering of the board, pieces, highlights, and user messages.
"""
class Graphics:
	def __init__(self):
		"""Initializes the graphics of the board and loads resources."""

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

	
	def set_caption(self, caption):
		"""Update the window title"""
		self.caption = caption
		pygame.display.set_caption(caption)


	def setup_window(self):
		"""Initializing window"""
		pygame.init()
		pygame.mixer.init()
		pygame.display.set_caption(self.caption)

		self.move_sound = pygame.mixer.Sound("resources/move_sound.wav")

    
	def update_display(self, board, legal_moves, selected_piece):
		"""updating the visuals of the board"""
		self.screen.blit(self.background, (0,0))
		
		self.highlight_squares(legal_moves, selected_piece)
		self.draw_board_pieces(board)
		if self.message:
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)

		pygame.display.update()
		self.clock.tick(self.fps)


	def draw_board_squares(self, board):
		"""Drawing squares (place where the piece can be put)"""
		for x in range(8):
			for y in range(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )
	
    
	def draw_board_pieces(self, board):
		"""Drawing pieces on the board (normal ones and kings)"""
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


    
	def pixel_coords(self, board_coords):
		"""center pixel of board's squares"""
		return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

    
	def board_coords(self, pixel):
		"""convert pixel coord, to square coords (we know on which square we click)"""
		return (pixel[0] // self.square_size, pixel[1] // self.square_size)

    
	def highlight_squares(self, squares, origin):
		"""highliting the squares (board) (for possible moves)"""
		for square in squares:
			pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))	

		if origin != None:
			pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

    
    
	def draw_message(self, message):
		"""Draws message to the screen"""
		self.message = True
		self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (self.window_size >> 1, self.window_size >> 1)
