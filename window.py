import pygame
import sys
import os

from Game import Game
from screen_setup import SCREEN_WIDTH, SCREEN_HEIGHT
from Board import Board


# Initialize Pygame
pygame.init()

# Set up window position
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400,0)
# Set up window dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Start Game
game = Game(pygame, screen)
game.loop(pygame, screen)

print("Bye")
# Quit Pygame
pygame.quit()
sys.exit()
