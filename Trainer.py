import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from DQN import DQN
import screen_setup

class Trainer:
    def __init__(self):
        self.model = DQN()

    def board_to_tensor(self, board, object):
        board_list = [
            [0 if board[y][x].accessible == 0 or (x, y) in object.pos else 1 for x in range(screen_setup.x_boxes)] for y
            in range(screen_setup.y_boxes)]

        numpy_array = np.array(board_list, dtype=np.float32)
        tensor_board = torch.tensor(numpy_array.flatten())
        return tensor_board

    def train(self, board, object):
        state_tensor = self.board_to_tensor(board, object)
        q_values = self.model(state_tensor)  # Predict Q-values

        action = torch.argmax(q_values).item()
        print(action)
        return action