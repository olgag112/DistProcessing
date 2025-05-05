import pygame, sys
from pygame.locals import *
import random

from graphics import Graphics
from board import Board
from server import Server
from client import Client

#Colors
WHITE    = (196, 158, 119)
BLUE     = (255, 255, 255)
RED      = (0,   0,   0)
BLACK    = (  0,   0,   0)
GOLD     = (255, 215,   0)
HIGH     = (160, 190, 255)

class Game:
	"""
	The main game control.
	"""

	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()

		self.selected_piece = None # a board location. 
		self.hop = False
		self.selected_legal_moves = []

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

		self.my_color = BLUE if self.is_server else RED
	#	self.turn = BLUE if self.is_server else RED

	def make_network_move(self):
		"""
        Sends the move to the opponent.
        """
		# self.network.send((start_pos, end_pos))
		self.network.send(self.board)

	def receive_network_move(self):
		"""
        Receives a move from the opponent and applies it.
        """
		try:
			# Receive data from the network
			received_board = self.network.receive()

			if received_board == "QUIT":
				self.graphics.draw_message("Opponent quit the game.")
				pygame.time.delay(3000) 
				self.terminate_game()
				return
			
			if isinstance(received_board, Board):
				self.board = received_board
				self.my_turn = True

			else:
				print("Received invalid data")

		except Exception as e:
			print("Error in receiving move:", e)
			print("Connection lost")
			self.terminate_game()

	# def receive_network_move(self):
	# 	"""
    #     Receives a move from the opponent and applies it.
    #     """
	# 	try:
	# 		move = self.network.receive()
	# 		if move:
	# 			start, end = move
	# 			self.board.move_piece(start, end)
	# 			if end not in self.board.adjacent(start):
	# 				self.board.remove_piece(((start[0] + end[0]) >> 1, (start[1] + end[1]) >> 1))
	#
	# 			self.turn = self.my_color
	# 			self.my_turn = True
	#
	# 	except:
	# 		print("Connection lost")
	# 		self.terminate_game()

	def setup(self):
		"""Draws the window and board at the beginning of the game"""
		self.graphics.setup_window()
		self.update()

	# def setup_network(self):
	# 	is_host = input("Host or Join? (h/j): ").strip().lower() == 'h'
	# 	self.is_server = is_host
	#
	# 	if is_host:
	# 		self.network = Server(port=5555)
	# 		self.my_turn = random.choice([True, False])
	# 		self.network.send(self.my_turn)
	# 		self.my_color = BLUE if self.my_turn else RED
	# 		pygame.display.set_caption("Checkers - Host")
	# 	else:
	# 		ip = input("Enter host IP: ")
	# 		self.network = Client(ip, port=5555)
	# 		self.my_turn = self.network.receive()
	# 		self.my_color = RED if self.my_turn else BLUE
	# 		pygame.display.set_caption("Checkers - Client")
	#
	# 	print(
	# 		f"Game started! You are {'BLUE' if self.my_color == BLUE else 'RED'} and it's {'your' if self.my_turn else 'opponent'} turn.")

	# def start_listener(self):
	# 	def listen():
	# 		while True:
	# 			move = self.network.receive()
	# 			if move:
	# 				self.move_queue.append(move)
	#
	# 	threading.Thread(target=listen, daemon=True).start()

	def event_loop(self):
		"""
		The event loop. This is where events are triggered 
		(like a mouse click) and then effect the game state.
		"""
		self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos()) # what square is the mouse in?


		if self.selected_piece != None:
			self.selected_legal_moves = self.board.legal_moves(self.selected_piece, self.hop)

		for event in pygame.event.get():

			if event.type == QUIT:
				self.terminate_game()

			if event.type == KEYDOWN:
				if event.key == K_q:
					self.terminate_game()

			if event.type == MOUSEBUTTONDOWN:
				# if self.turn != self.my_color:
				# 	# 🔒 Block input if it's not your turn
				# 	return
				if not self.my_turn:
					return
				if self.hop == False:
					# if self.board.location(self.mouse_pos).occupant != None and self.board.location(self.mouse_pos).occupant.color == self.turn:
					# 	self.selected_piece = self.mouse_pos
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
							#self.board.move_piece(self.selected_piece, self.mouse_pos)

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

	def update(self):
		"""Calls on the graphics class to update the game display."""
		self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)

	def terminate_game(self):
		"""Quits the program and ends the game."""
		try:
			if self.network:
				self.network.send("QUIT")
		except:
			pass 

		pygame.quit()
		sys.exit()

	def main(self):
		"""This executes the game and controls its flow."""
		self.setup()

		while True:  # Main game loop
			if self.my_turn:
				# It's the current player's turn, process player input
				self.update()
				self.event_loop()  # Handle player input (mouse click, etc.)
				self.update()  # Update the display
			else:
				self.receive_network_move()

	# def main(self):
	# 	""""This executes the game and controls its flow."""
	# 	self.setup()
	# 	#self.setup_network()
	# 	#self.start_listener()
	#
	# 	if self.is_server:
	# 		self.my_turn = random.choice([True, False])  # Assign turn randomly if server
	# 		self.network.send(self.my_turn)  # Send turn to client
	# 	else:
	# 		self.my_turn = self.network.receive()  # Get turn from the server (client side)
	#
	# 	while True:  # Main game loop
	# 		if self.my_turn:
	# 			# It's the current player's turn
	# 			self.event_loop()  # Handle player input (mouse click, etc.)
	# 			self.update()  # Update the display
	# 		else:
	# 			# Wait for move from the opponent
	# 			move = self.network.receive()
	# 			if move and isinstance(move, tuple) and len(move) == 2:
	# 				start, end = move
	# 				self.board.move_piece(start, end)
	# 				if end not in self.board.adjacent(start):
	# 					self.board.remove_piece(((start[0] + end[0]) >> 1, (start[1] + end[1]) >> 1))
	# 				self.turn = self.my_color  # Switch to your turn
	# 				self.my_turn = True  # Your turn now
	# 			else:
	# 				# Unexpected move data received
	# 				print(f"Unexpected data received: {move}")
	#
	# 		self.event_loop()
	# 		self.update()

	def end_turn(self):
		"""
		End the turn. Switches the current player. 
		end_turn() also checks for and game and resets a lot of class attributes.
		"""

		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False
		self.my_turn = False
		role = "Host" if self.is_server else "Client"
		self.graphics.set_caption(f"Checkers - {role} - Opponent's Turn")
		if self.check_for_endgame():
			winner = "BLUE" if self.my_color != BLUE else "RED"
			self.graphics.draw_message(f"{winner} WINS!")
			return
		
	

	def check_for_endgame(self):
		"""
		Checks if the opponent has any legal moves left.
		If not, the game is over.
		"""
		opponent_color = RED if self.my_color == BLUE else BLUE

		for x in range(8):
			for y in range(8):
				loc = self.board.location((x, y))
				if loc.color == BLACK and loc.occupant is not None and loc.occupant.color == opponent_color:
					if self.board.legal_moves((x, y)) != []:
						return False  # Opponent still has a legal move
		return True  # Opponent has no legal moves or pieces

# def check_for_endgame(self):
	# 	"""
	# 	Checks to see if a player has run out of moves or pieces. If so, then return True. Else return False.
	# 	"""
	# 	for x in range(8):
	# 		for y in range(8):
	# 			if self.board.location((x,y)).color == BLACK and self.board.location((x,y)).occupant != None and self.board.location((x,y)).occupant.color == self.turn:
	# 				if self.board.legal_moves((x,y)) != []:
	# 					return False
	#
	# 	return True
