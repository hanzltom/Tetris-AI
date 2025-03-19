from Board import Board
from colors import COLORS
from screen_setup import *
from Trainer import Trainer, board_to_tensor
import time
import numpy as np
import random
from collections import deque

MEMORY_SIZE = 10000
BATCH_SIZE = 64

replay_memory = deque(maxlen=MEMORY_SIZE)  # Store (state, action, reward, next_state, done)


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
            episodes = 1000
            EPSILON = 1
            for episode in range(episodes):
                new_object = None
                state = None
                running = True
                create_new_object = True # if needed to create new object
                done = False
                total_reward = 0
                while running:

                    if self.board.is_out(): # if there is any object outside of zone
                        break

                    if create_new_object:
                        create_new_object = False
                        object_valid, new_object = self.board.create_object()
                        while not object_valid: # Object could not be created, creating different objects
                            object_valid, new_object = self.board.create_object()
                        state = board_to_tensor(self.board.board, new_object)

                    # Print board and object
                    self.board.print_board(pygame, surface, new_object)

                    # Select action using ε-greedy policy
                    if np.random.rand() < EPSILON:
                        action = np.random.randint(0, 5)  # Random action
                    else:
                        action = self.trainer.get_action(state)

                    reward, create_new_object = self.board.apply_action(new_object, action, pygame, surface)
                    next_state = board_to_tensor(self.board.board, new_object)

                    if self.board.is_out():  # if there is any object outside of zone
                        done = True

                    replay_memory.append((state, action, reward, next_state, done))




        except Exception as e:
            print(f"Error: {e}")

