import pygame, sys
from pygame.locals import *
import random

from graphics import Graphics
from board import Board
from server import Server
from client import Client

#Colors
WHITE    = (255, 255, 255)
BLACK    = (0,   0,   0)

# Class that handles the whole checker's logics
class Game:

	def __init__(self):
		
		self.graphics = Graphics()
		self.board = Board()

		self.selected_piece = None # a board location. 
		self.hop = False
		self.selected_legal_moves = []

		# variables used for server x client interactions
		self.is_server = None
		self.network = None
		self.my_turn = None
		self.move_queue = []

		# Networking setup
		is_server = input("Host or Join? (h/j): ").strip().lower() == 'h'

		if is_server:
			print("Waiting for opponent...")
			self.network = Server()
			self.my_turn = True
			self.network.send(self.my_turn)
		else:
			ip = input("Enter server IP: ")
			self.my_turn = False
			self.network = Client(ip)

		if is_server:
			self.graphics.set_caption("Checkers - Host")
		else:
			self.graphics.set_caption("Checkers - Client")

		self.is_server = is_server

		self.my_color = WHITE if self.is_server else BLACK

	# sending board to the opponent
	def make_network_move(self):
		"""
        Sends the move to the opponent.
        """
		# self.network.send((start_pos, end_pos))
		self.network.send(self.board)

	# Receives a move from the opponent
	def receive_network_move(self):
		try:
			# Receive data from the network
			received_board = self.network.receive()

			if received_board == "QUIT":
				self.graphics.draw_message("Opponent quit the game.")
				self.update()
				pygame.time.delay(3000) 
				self.terminate_game()
				return
			
			if isinstance(received_board, Board):
				self.board = received_board
				white_pieces = sum(1 for x in range(8) for y in range(8) if self.board.location((x,y)).occupant and self.board.location((x,y)).occupant.color == self.my_color)

				if white_pieces == 0:
					winner = "BLACK" if self.my_color == WHITE else "WHITE"
					self.graphics.draw_message(f"{winner} WINS!!!")
					self.update()
					
				self.my_turn = True

			else:
				print("Received invalid data")

		except Exception as e:
			print("Error in receiving move:", e)
			print("Connection lost")
			self.terminate_game()

	# creates a window where the board is displayed (beginning)
	def setup(self):
		self.graphics.setup_window()
		self.update()

	# handling the events (move, closing window, etc.)
	def event_loop(self):
		self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos()) # what square is the mouse in?


		if self.selected_piece != None:
			self.selected_legal_moves = self.board.legal_moves(self.selected_piece, self.hop)

		for event in pygame.event.get():

			# CLOSING WINDOW
			if event.type == QUIT:
				self.terminate_game()

			if event.type == KEYDOWN:
				if event.key == K_q:
					self.terminate_game()

			# Clicking on screen 
			if event.type == MOUSEBUTTONDOWN:
				if not self.my_turn:
					return
				# 
				if self.hop == False:
					piece = self.board.location(self.mouse_pos).occupant

					if piece is not None and piece.color == self.my_color: #and self.turn == self.my_color:
						self.selected_piece = self.mouse_pos

					elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece):

						self.board.move_piece(self.selected_piece, self.mouse_pos)
					
						if self.mouse_pos not in self.board.adjacent(self.selected_piece):
							self.board.remove_piece(((self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1))
							self.hop = True
							self.selected_piece = self.mouse_pos

						else:
							self.make_network_move()
							self.end_turn()

				if self.hop == True:
					if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece, self.hop):
						self.board.move_piece(self.selected_piece, self.mouse_pos)
						self.board.remove_piece(((self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1))

					if self.board.legal_moves(self.mouse_pos, self.hop) == []:
							self.make_network_move()
							self.end_turn()

					else:
						self.selected_piece = self.mouse_pos

		self.update()

	# diplaying updated board
	def update(self):
		self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)

	# quiting the game
	def terminate_game(self):
		try:
			if self.network:
				self.network.send("QUIT")
				self.end_turn()
		except:
			pass 

		pygame.quit()
		sys.exit()

	# handles the whole game's process
	def main(self):
		self.setup()

		while True:  # Main game loop
			if self.my_turn:
				# Turn
				self.update()
				self.event_loop()
				self.update()  
			else:
				self.receive_network_move()

	# end the turn. Switches the current player. 
	# end_turn() also checks for and game and resets a lot of class attributes.
	def end_turn(self):
		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False
		self.my_turn = False
		role = "Host" if self.is_server else "Client"
		self.graphics.set_caption(f"Checkers - {role} - Opponent's Turn")
		if self.check_for_endgame():
			winner = "BLACK" if self.my_color != WHITE else "WHITE"
			self.network.send("LOSS")
			self.graphics.draw_message(f"{winner} WINS!")
			return
		
	
	# Checks if the opponent has any possible moves left.
	# If not, the game is over.
	def check_for_endgame(self):

		opponent_color = BLACK if self.my_color == WHITE else WHITE

		for x in range(8):
			for y in range(8):
				loc = self.board.location((x, y))
				if loc.color == BLACK and loc.occupant is not None and loc.occupant.color == opponent_color:
					if self.board.legal_moves((x, y)) != []:
						return False  # Opponent still has a legal move
		return True  # Opponent has no legal moves or pieces