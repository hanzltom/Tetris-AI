import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import screen_setup

input_size = screen_setup.x_boxes * screen_setup.y_boxes

class DQN(nn.Module):
    """
    Class representing the Deep Q-Learning Neural Network
    """
    def __init__(self):
        super(DQN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)  # output size (32, 21, 11)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)  # output size (64, 21, 11)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)  # output size (64, 21, 11)

        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(64 * input_size, 512)
        self.fc2 = nn.Linear(512, 5)

        self.optimizer = optim.Adam(self.parameters(), lr=0.001)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = self.flatten(x)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)
