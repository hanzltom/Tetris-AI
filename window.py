import pygame
import sys
import os
from colors import COLORS
from screen_setup import SCREEN_WIDTH, SCREEN_HEIGHT
from Board import Board


# Initialize Pygame
pygame.init()

# Set up window position
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400,0)
# Set up window dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

#Board
board = Board()

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(COLORS["BLACK"])
    board.print(pygame, screen)
    board.print_lines(pygame, screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
