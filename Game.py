from Board import Board
from colors import COLORS
from screen_setup import *

class Game:
    def __init__(self, pygame, surface):
        self.board = Board()
        self.board.first_print(pygame, surface)
        pygame.display.flip()


    def loop(self, pygame, surface):
        input("Press Enter to continue")
        running = True
        new_object = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            print("Finding new object")
            object_valid, new_object = self.board.create_object()
            while not object_valid:
                print("New object is invalid")
                object_valid, new_object = self.board.create_object()
            print("Valid object found")
            new_object.print(self.board.board, pygame, surface)
            self.board.print_lines(pygame, surface)
            # Update the display
            pygame.display.flip()
            input("Press Enter to continue")