# Tetris-AI - Reinforcement learning

This project implements a Deep Q-Network (DQN) agent trained to play a Tetris game using PyTorch and Pygame. The agent learns through reinforcement learning by interacting with the environment and improving over time.

## Features

- Custom block-stacking environment built with Pygame
- Deep Q-Learning agent using convolutional neural networks (CNNs)
- Training from raw board states (as images or grids)
- Reward shaping based on placement and line clearing
- Experience replay and epsilon-greedy policy

The perfect model is still not ready, since it takes a lot of training time to get to a optimal state.

---

The branch called **game_for_one** can be used for classic game of Tetris for one player


---

## How to run
```bash
   python3 main.py
````

***Possible arguments***

Enable training mode with new model (default):
>--train0


Enable training mode with previously saved model:
>--train1


Let the model start playing (TODO):
>--play



Display help message:
>--help



     