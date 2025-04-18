import pygame
import sys
import os
from Game import Game
from screen_setup import SCREEN_WIDTH, SCREEN_HEIGHT
import torch

try:
    old_model_usage = False
    if len(sys.argv) > 0:
        if int(sys.argv[1]) == 1:
            print("tady")
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
    game.loop(pygame, screen)

    # Quit Game
    pygame.quit()
    sys.exit()

except KeyboardInterrupt as e:
    print(e)
    save = None
    while save != 1 and save != 0:
        save = int(input("Do you want to save the model? 1/0: "))
    if save == 1:
        torch.save(game.trainer.model.state_dict(), "tetris_dqn.pth")
