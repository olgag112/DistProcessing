import pygame, sys
from pygame.locals import *

from game import Game

pygame.font.init()

def main():
	game = Game()
	game.main()

if __name__ == "__main__":
	main()