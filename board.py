from square import Square
from piece import Piece

#Colors
BROWN    = (255, 255, 255)
WHITE     = (255, 255, 255)
BLACK      = (0,   0,   0)
LIGHT_BROWN  = (0,0,0)


#Moves
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"


"""
Represents a checkers game board with an 8x8 matrix of 'Square' objects , 
"""
class Board:
	def __init__(self):
		"""Initializes the board by creating and populating the matrix with pieces."""
		self.matrix = self.new_board()


	def new_board(self):
		"""Creates a new board and allocate pieces for players """
		matrix = [[None] * 8 for i in range(8)]

		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(BROWN)
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(LIGHT_BROWN)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(BROWN)
				elif (x % 2 == 0) and (y % 2 == 0): 
					matrix[y][x] = Square(LIGHT_BROWN)

		# initialize the pieces and put them in the appropriate squares
		for x in range(8):
			for y in range(3):
				if matrix[x][y].color == LIGHT_BROWN:
					matrix[x][y].occupant = Piece(BLACK)
			for y in range(5, 8):
				if matrix[x][y].color == LIGHT_BROWN:
					matrix[x][y].occupant = Piece(WHITE)

		return matrix
	
	def rel(self, dir, pixel):
		"""Returns the relative position from a pixel in the given diagonal direction"""
		x = pixel[0]
		y = pixel[1]
		if dir == NORTHWEST:
			return (x - 1, y - 1)
		elif dir == NORTHEAST:
			return (x + 1, y - 1)
		elif dir == SOUTHWEST:
			return (x - 1, y + 1)
		elif dir == SOUTHEAST:
			return (x + 1, y + 1)
		else:
			return 0


	def adjacent(self, pixel):
		"""Returns a list of squares locations that are adjacent (on a diagonal) to (x,y)."""
		x = pixel[0]
		y = pixel[1]

		return [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y)),self.rel(SOUTHWEST, (x,y)),self.rel(SOUTHEAST, (x,y))]


	def location(self, pixel):
		"""Return the square from the board based on coordinates (pixel)"""
		x = pixel[0]
		y = pixel[1]

		return self.matrix[x][y]
	

	def blind_legal_moves(self, pixel):
		"""Returns list of possible directions (without checking if its possible)"""
		x = pixel[0]
		y = pixel[1]
		if self.matrix[x][y].occupant != None:
			
			if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == WHITE:
				blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y))]
				
			elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == BLACK:
				blind_legal_moves = [self.rel(SOUTHWEST, (x,y)), self.rel(SOUTHEAST, (x,y))]

			else:
				blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y)), self.rel(SOUTHWEST, (x,y)), self.rel(SOUTHEAST, (x,y))]

		else:
			blind_legal_moves = []

		return blind_legal_moves


	def legal_moves(self, pixel, to_select = None, hop = False):
		"""Returns a list of possible move locations from a given set of coordinates (x,y) on the board."""
		self.can_hop = False
		if to_select and pixel not in to_select:
			return []
		x = pixel[0]
		y = pixel[1]
		blind_legal_moves = self.blind_legal_moves((x,y)) 
		legal_moves = []

		if hop == False:
			for move in blind_legal_moves:
				if hop == False:
					if self.on_board(move):
						if self.location(move).occupant == None:
							legal_moves.append(move)

						elif self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
							legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
							self.can_hop = True
							

		else: # hop == True
			for move in blind_legal_moves:
				if self.on_board(move) and self.location(move).occupant != None:
					if self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
						legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))
						self.can_hop = True
					
		if self.can_hop:
			legal_moves = [moves for moves in legal_moves if moves not in blind_legal_moves]
		return legal_moves


	def remove_piece(self, pixel):
		"""Removes a piece from the board at position (x,y)"""
		x = pixel[0]
		y = pixel[1]
		self.matrix[x][y].occupant = None


	def move_piece(self, pixel_start, pixel_end):
		"""moves a piece fromm pixel_start to pixel_end"""
		start_x = pixel_start[0]
		start_y = pixel_start[1]
		end_x = pixel_end[0]
		end_y = pixel_end[1]

		self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
		self.remove_piece((start_x, start_y))

		self.king((end_x, end_y))


	# Is passed a coordinate tuple (x,y), and returns true or 
	# false depending on if that square on the board is an end square.
	def is_end_square(self, coords):

		if coords[1] == 0 or coords[1] == 7:
			return True
		else:
			return False


	def on_board(self, pixel):
		"""Checks to see if the given square (x,y) lies on the board"""

		x = pixel[0]
		y = pixel[1]
		if x < 0 or y < 0 or x > 7 or y > 7:
			return False
		else:
			return True


	def king(self, pixel):
		"""Takes in (x,y), the coordinates of square to be considered for kinging"""
		x = pixel[0]
		y = pixel[1]
		if self.location((x,y)).occupant != None:
			if (self.location((x,y)).occupant.color == WHITE and y == 0) or (self.location((x,y)).occupant.color == BLACK and y == 7):
				self.location((x,y)).occupant.king = True 

	def capture_posibility(self, color):
		"""Returns all pieces of a given color that have at least one legal capture move."""
		to_select = []
		for i in range(8):
			for j in range(8):
				square = self.location((i, j))
				if square.occupant and square.occupant.color == color:
					self.legal_moves((i,j))
					if self.can_hop:
						to_select.append((i,j))
		return to_select	
