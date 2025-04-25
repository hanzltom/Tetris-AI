import pygame
import sys
import os
import traceback
from Game import *
from screen_setup import SCREEN_WIDTH, SCREEN_HEIGHT

try:
    old_model_usage = False
    if len(sys.argv) > 0:
        if int(sys.argv[1]) == 1:
            old_model_usage = True

    # Initialize Pygame
    pygame.init()

    # Set up window position
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400,0)
    # Set up window dimensions
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    # Start Game
    game = Game(pygame, screen, old_model_usage)
    game.loop(pygame, screen, old_model_usage)

    # Quit Game
    pygame.quit()
    sys.exit()

except Exception as e:
    print(f"Error: {e}")
    print(traceback.format_exc())
