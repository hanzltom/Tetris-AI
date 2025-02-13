from Board import Board
from colors import COLORS
from screen_setup import *

class Game:
    def __init__(self, pygame, surface):
        self.board = Board()
        self.board.first_print(pygame, surface)


    def loop(self, pygame, surface):
        running = True
        new_object = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            #self.board.create_object()
            # Update the display
            pygame.display.flip()