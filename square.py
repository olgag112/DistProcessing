"""
Class represents a square on the board
"""
class Square:
	def __init__(self, color, occupant = None):
		self.color = color
		self.occupant = occupant # occupant is a Square object
