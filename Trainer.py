import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from DQN import DQN
import screen_setup


class Trainer:
    def __init__(self):
        self.model = DQN()

    def get_action(self, state_tensor):
        q_values = self.model(state_tensor)  # Predict Q-values

        action = torch.argmax(q_values).item()
        print(action)
        return action

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

