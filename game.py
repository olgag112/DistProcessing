import asyncio
import os
import pygame, sys
from pygame.locals import *
import random
import threading

from graphics import Graphics
from board import Board
from server import *

#Colors
WHITE    = (255, 255, 255)
BLACK    = (0,   0,   0)

"""
Class that handles the whole game process
"""
class Game:

	def __init__(self, network, is_server):
		"""initializing the game for one player"""
		
		self.graphics = Graphics()
		self.board = Board()

		self.selected_piece = None # a board location. 
		self.hop = False # enable capturing multiple pieces in one round
		self.selected_legal_moves = [] # stores possible moves for selected piece

		# variables used for server x client interactions
		self.is_server = is_server
		self.network = network
		self.my_turn = False

		# used for capture piece obligation
		self.capture_posibility = []


		if is_server:
			self.my_turn = True
			self.my_color = WHITE
		else:
			self.my_color = BLACK
			
		self.role = "WHITE" if self.is_server else "BLACK"
		self.graphics.set_caption(f"Checkers - {self.role}")


	async def make_network_move(self):
		"""sending board to the opponent"""
		await self.network.send(self.board)


	async def receive_network_move(self):
		"""Receives a move from the opponent"""
		try:
			# Receive data from the network
			received_board = await self.network.receive()
			# if user closes a window
			if received_board == "QUIT":
				self.graphics.draw_message("Opponent quit the game.")
				self.update()
				pygame.time.delay(3000)  # wait 3 sec to close the window
				pygame.quit()
				os.exit(0)
				return 

			# if other player made a move and the whole board was sent via network
			if isinstance(received_board, Board):
				self.board = received_board
				pieces_left = sum(1 for x in range(8) for y in range(8) if self.board.location((x, y)).occupant and self.board.location((x, y)).occupant.color == self.my_color)

				# checking if the player has some pieces left on the board
				# if not -> game ends
				if pieces_left == 0:
					winner = "BLACK" if self.my_color == WHITE else "WHITE"
					self.graphics.draw_message(f"{winner} WINS!!!")
					self.update()
					pygame.time.delay(10000)

				# when receiving the board and updating it
				# system checks if there are any possible captures
				# if so -> player is obligated to capture a piece
				self.capture_posibility = self.board.capture_posibility(self.my_color)
					
				self.my_turn = True

			else:
				print("Received invalid data")

		except Exception as e:
			print("Error in receiving move:", e)
			print("Connection lost")
			await self.terminate_game()


	def setup(self):
		"""creates a window where the board is displayed (beginning)"""
		self.graphics.setup_window()
		self.update()

	
	async def event_loop(self):
		"""handling the events (move, closing window, etc.)"""
		self.update()
		# what square is the mouse in?
		self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos())


		if self.selected_piece != None:
			self.selected_legal_moves = self.board.legal_moves(self.selected_piece,self.capture_posibility, self.hop)

		for event in pygame.event.get():

			# CLOSING WINDOW
			if event.type == QUIT:
				await self.terminate_game()

			if event.type == KEYDOWN:
				if event.key == K_q:
					await self.terminate_game()

			# Clicking on screen 
			if event.type == MOUSEBUTTONDOWN:
				# if it's not your turn -> do nothing
				if not self.my_turn:
					return
				
				# move
				if self.hop == False:
					piece = self.board.location(self.mouse_pos).occupant

					if piece is not None and piece.color == self.my_color:
						self.selected_piece = self.mouse_pos

					elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece, self.capture_posibility):

						self.board.move_piece(self.selected_piece, self.mouse_pos)
					
						if self.mouse_pos not in self.board.adjacent(self.selected_piece):
							self.board.remove_piece(((self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1))
							self.hop = True
							self.capture_posibility = []
							self.graphics.move_sound.play()
							self.selected_piece = self.mouse_pos

						else:
							await self.make_network_move()
							await self.end_turn()

				# if the player has already captured piece in this turn
				if self.hop == True:
					if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece,self.capture_posibility, self.hop):
						self.board.move_piece(self.selected_piece, self.mouse_pos)
						self.board.remove_piece(((self.selected_piece[0] + self.mouse_pos[0]) >> 1, (self.selected_piece[1] + self.mouse_pos[1]) >> 1))

					if self.board.legal_moves(self.mouse_pos,self.capture_posibility, self.hop) == []:
							await self.make_network_move()
							await self.end_turn()

					else:
						self.selected_piece = self.mouse_pos
		self.update()


	def update(self):
		"""updating board"""
		self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)


	async def terminate_game(self):
		"""quiting the game"""
		# inform opponent that you left and terminate the code
		try:
			if self.network:
				await self.network.send("QUIT") 
				await asyncio.sleep(0.5)      
		except Exception as e:
			print("Error sending QUIT:", e)
		finally:
			pygame.quit()
			os._exit(0)


	async def main(self):
		"""handles the whole game's process"""
		self.setup()

		# process of the game
		while True:
			if self.my_turn:
				# If it's your turn
				self.update()
				await self.event_loop()
				self.update()  
			else:
				# Waiting for another player's move
				await self.receive_network_move()


	async def end_turn(self):
		"""
		End the turn. Switches the current player. 
		Checks if the game ended
		"""
		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False
		self.my_turn = False
		self.update()
		pygame.display.update()
		await asyncio.sleep(0)  
		

		self.graphics.move_sound.play()
		if self.check_for_endgame():
			winner = BLACK if self.my_color != WHITE else WHITE
			await self.network.send("LOSS")
			self.graphics.draw_message(f"{self.role} WINS!")
			return
		
	
	def check_for_endgame(self):
		"""
		Checks if the opponent has any possible moves left.
		If not, the game is over.
		"""
		opponent_color = BLACK if self.my_color == WHITE else WHITE
		for x in range(8):
			for y in range(8):
				loc = self.board.location((x, y))
				if loc.color == BLACK and loc.occupant is not None and loc.occupant.color == opponent_color:
					if self.board.legal_moves((x, y)) != []:
						return False 
		return True 
