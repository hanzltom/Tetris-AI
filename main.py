import pygame
import sys
import os
import argparse
import traceback
from Game import *
from screen_setup import SCREEN_WIDTH, SCREEN_HEIGHT

parser = argparse.ArgumentParser()
parser.add_argument('--train0', action='store_true', help='Enable training mode with new model')
parser.add_argument('--train1', action='store_true', help='Enable training mode with saved model')
parser.add_argument('--play', action='store_true', help='Let the model start playing')
args = parser.parse_args()

try:
    old_model_usage = False

    if args.train1:
        print("Training with saved model")
        old_model_usage = True
    elif args.play:
        print("Playing")
    else:
        print("Training with new model")

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
