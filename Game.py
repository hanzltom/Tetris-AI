from Board import Board
from colors import COLORS
from screen_setup import *
from Trainer import Trainer, board_to_tensor
import time
import numpy as np
import random
import json
import pickle
from collections import deque
import torch
import torch.optim as optim
import more_itertools as mit
import traceback
import logging

MEMORY_SIZE = 10000
BATCH_SIZE = 64
GAMMA = 0.99

EPSILON = 1.0
EPSILON_DECAY = 0.995
EPSILON_MIN = 0.05
EPISODES = 10000

# used for saving to a json file
CURRENT_EPISODE = 0
CURRENT_SUM_OF_REWARDS = 0

# Create and configure logger
logging.basicConfig(filename="logs.log", format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
tuple_sum_by_indices = lambda x, y: tuple(a + b for a, b in zip(x, y))

replay_memory = deque(maxlen=MEMORY_SIZE)  # Store (state, action, reward, next_state, done)


class Game:
    """
    Class Game which serves as the main game loop calling other methods
    """
    def __init__(self, pygame, surface, old_model_usage):
        """
        Constructor of Game for setting the Board and printing it
        :param pygame: Pygame object
        :param surface: Surface object for printing
        :param old_model_usage: Bool if to import old model
        """
        self.board = Board()
        self.board.print_board(pygame, surface)
        pygame.display.flip()
        self.trainer = Trainer(old_model_usage)

        if old_model_usage:
            global replay_memory
            replay_memory = pickle.load(open('replay_memory.pkl', 'rb'))


    def loop(self, pygame, surface, old_model_usage):
        """
        Function loop managing the game
        :param pygame: Pygame object
        :param surface: Surface object for printing
        :param old_model_usage: Bool if to import old model
        :return: None
        """
        try:
            global EPSILON
            episode_old, sum_of_rewards = 0, 0

            if old_model_usage:
                episode_old, sum_of_rewards, EPSILON = self.read_json()

            for episode in range(episode_old, EPISODES):
                global CURRENT_EPISODE, CURRENT_SUM_OF_REWARDS
                CURRENT_EPISODE = episode
                CURRENT_SUM_OF_REWARDS = sum_of_rewards

                new_object = None
                state = None
                create_new_object = True # if needed to create new object
                done = False
                total_reward, round_counter = 0, 0
                episode_reward_sum = (0,0,0,0,0,0,0)
                while True:

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

                    # Select action using epsilon greedy policy
                    if np.random.rand() < EPSILON:
                        actions = list(mit.random_permutation(range(5))) # Get random permutation
                    else:
                        actions = self.trainer.get_action(state)

                    # Move the object and get the reward
                    reward, create_new_object, action, log_reward = self.board.apply_action(new_object, actions, pygame, surface)
                    next_state = board_to_tensor(self.board.board, new_object)

                    if self.board.is_out():  # if there is any object outside of zone
                        done = True

                    # Save all of this to the memory
                    replay_memory.append((state, action, reward, next_state, done))

                    # Train the model on random batch sample
                    self.trainer.train(replay_memory, BATCH_SIZE, GAMMA)

                    state = next_state
                    total_reward += reward
                    round_counter += 1
                    episode_reward_sum = tuple_sum_by_indices(log_reward, episode_reward_sum)

                # Lower the epsilon to prefer actions from the memory over random actions
                if EPSILON > EPSILON_MIN:
                    EPSILON *= EPSILON_DECAY

                self.board = Board() # reset board for new episodes
                sum_of_rewards += total_reward

                print(f"Episode: {episode} out of {EPISODES}, reward: {sum_of_rewards:.1f}, epsilon: {EPSILON}")
                logger.info(f"Episode: {episode}, sum: {sum_of_rewards:.1f}, number_of_rounds: {round_counter} "
                            f"REWARDS: [lines: {episode_reward_sum[0]:.1f}, gaps: {episode_reward_sum[1]:.1f}, "
                            f"height: {episode_reward_sum[2]:.1f}, tightness: {episode_reward_sum[3]:.1f}, "
                            f"closeness: {episode_reward_sum[4]:.1f}, centering: {episode_reward_sum[5]:.1f},"
                            f"coverage: {episode_reward_sum[6]:.1f}]")


            torch.save(self.trainer.model.state_dict(), "tetris_dqn.pth") # Save the model


        except KeyboardInterrupt as e:
            print(e)
            save = None
            while save != 1 and save != 0:
                save = int(input("Do you want to save the model? 1/0: "))
            if save == 1:
                torch.save(self.trainer.model.state_dict(), "tetris_dqn.pth")

                dict_to_save = {
                    "episode": CURRENT_EPISODE,
                    "sum_of_rewards": CURRENT_SUM_OF_REWARDS,
                    "EPSILON": EPSILON,
                }
                with open("sample.json", "w") as outfile:
                    json.dump(dict_to_save, outfile)

                pickle.dump(replay_memory, open('replay_memory.pkl', 'wb'))

    def read_json(self):
        with open('sample.json', ) as file:
            data = json.load(file)
            return data["episode"], data["sum_of_rewards"], data["EPSILON"]