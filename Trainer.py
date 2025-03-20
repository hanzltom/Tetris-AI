from random import random

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from DQN import DQN
import screen_setup
import random


class Trainer:
    def __init__(self):
        self.model = DQN()
        if int(input("Do you want to load the model? 1/0: ")) == 1:
            print("Using saved model")
            self.model.load_state_dict(torch.load("tetris_dqn.pth"))


    def get_action(self, state_tensor):
        q_values = self.model(state_tensor)  # Predict Q-values

        action = torch.argmax(q_values).item()
        return action

    def train(self, replay_memory, BATCH_SIZE, GAMMA):
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        if len(replay_memory) < BATCH_SIZE:
            return # Not enough data in memory

        batch = random.sample(replay_memory, BATCH_SIZE)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.stack(states)
        next_states = torch.stack(next_states)
        actions = torch.tensor(actions, dtype=torch.long).unsqueeze(1)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)

        with torch.no_grad():
            target_q_values = rewards + GAMMA * torch.max(self.model(next_states), dim=1)[0] * (1 - dones)

        predicted_q_values = self.model(states).gather(1, actions).squeeze(1)

        # Compute loss and update model
        loss = torch.nn.MSELoss()(predicted_q_values, target_q_values)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

def board_to_tensor(board, object = None):
    if object:
        board_list = [
            [0 if board[y][x].accessible == 0 or (x, y) in object.pos else 1 for x in range(screen_setup.x_boxes)] for y
            in range(screen_setup.y_boxes)]
    else:
        board_list = [
            [0 if board[y][x].accessible == 0  else 1 for x in range(screen_setup.x_boxes)]
            for y in range(screen_setup.y_boxes)]

    numpy_array = np.array(board_list, dtype=np.float32)
    tensor_board = torch.tensor(numpy_array.flatten())
    return tensor_board

