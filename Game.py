from Board import Board
from colors import COLORS
from screen_setup import *
from Trainer import Trainer
import time

class Game:
    """
    Class Game which serves as the main game loop calling other methods
    """
    def __init__(self, pygame, surface):
        """
        Constructor of Game for setting the Board and printing it
        :param pygame: Pygame object
        :param surface: Surface object for printing
        """
        self.board = Board()
        self.board.print_board(pygame, surface)
        pygame.display.flip()
        self.trainer = Trainer()


    def loop(self, pygame, surface):
        """
        Function loop managing the game
        :param pygame: Pygame object
        :param surface: Surface object for printing
        :return: None
        """
        try:
            drop_interval = 1500  # Time in milliseconds for automatic downward movement
            last_drop_time = pygame.time.get_ticks() # indicates how long it passed from the last drop of the object
            new_object = None
            running = True
            create_new_object = True # if needed to create new object
            while running:
                current_time = pygame.time.get_ticks()

                if self.board.is_out(): # if there is any object outside of zone
                    break

                if create_new_object:
                    create_new_object = False
                    object_valid, new_object = self.board.create_object()
                    while not object_valid: # Object could not be created, creating different objects
                        object_valid, new_object = self.board.create_object()

                # Print board and object
                self.board.print_board(pygame, surface, new_object)

                # Get input
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Allow multiple moves in one frame
                for _ in range(5):  # Adjust the number of moves per frame
                    action = self.trainer.train(self.board.board, new_object)
                    if action == 0:
                        self.board.move_object(new_object, "LEFT")
                    elif action == 1:
                        self.board.move_object(new_object, "RIGHT")
                    elif action == 2:
                        self.board.move_object(new_object, "DOWN")
                    elif action == 3:
                        self.board.rotate_piece(new_object, "RIGHT")
                    elif action == 4:
                        self.board.rotate_piece(new_object, "LEFT")
                    time.sleep(0.1)

                # If enough time passed, drop the object
                if current_time - last_drop_time > drop_interval:
                    if not self.board.move_object(new_object, "DOWN"): # If we cannot drop it further
                        self.board.lock_object(new_object)  # Lock object on the board
                        self.board.clear_lines(pygame, surface) # Clear full lines
                        create_new_object = True
                    last_drop_time = current_time



            input("Enter for exit")


        except Exception as e:
            print(f"Error: {e}")

