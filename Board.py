from logging import raiseExceptions

from objects.ObjectI import ObjectI
from objects.ObjectJ import ObjectJ
from objects.ObjectL import ObjectL
from objects.ObjectO import ObjectO
from objects.ObjectS import ObjectS
from objects.ObjectT import ObjectT
from objects.ObjectZ import ObjectZ
from objects.Object import Object
from screen_setup import SCREEN_WIDTH, SCREEN_HEIGHT, x_boxes, y_boxes
from Field import Field
from Position import Position
from colors import COLORS
import random
import time
import numpy as np

# List of all available objects
object_list = [ObjectI, ObjectJ, ObjectL, ObjectO, ObjectS, ObjectT, ObjectZ]

class Board:
    """
    Class Board representing the game board
    """
    def __init__(self):
        """
        Constructor creating the game board
        """
        self.board = [[]]

        for y in range(y_boxes):
            self.board.append([])
            for x in range(x_boxes):

                x_cor = SCREEN_WIDTH / x_boxes * x
                y_cor = SCREEN_HEIGHT / y_boxes * y

                if x == 0 or x == x_boxes - 1 or y == 0 or y == y_boxes - 1:
                    self.board[y].append(
                        Field(Position( x, y, (x_cor, y_cor), (SCREEN_WIDTH / x_boxes, SCREEN_HEIGHT / y_boxes)), False))
                else:
                    self.board[y].append(
                    Field(Position( x, y, (x_cor, y_cor), (SCREEN_WIDTH / x_boxes, SCREEN_HEIGHT / y_boxes)), True))


    def print_edges(self, pygame, surface):
        """
        Method to print the edges of the game board
        :param pygame: Pygame instance
        :param surface: Surface instance
        :return: None
        """
        [self.board[y][x].print(pygame, surface) for y in range(y_boxes) for x in range(x_boxes)]

    def print_lines(self, pygame, surface):
        """
        Method to print the lines of the game board
        :param pygame: Pygame instance
        :param surface: Surface instance
        :return: None
        """
        # Vertical lines
        for i in range(x_boxes):
            x_cor = SCREEN_WIDTH / x_boxes * i
            pygame.draw.line(surface, COLORS["WHITE"], (x_cor, 0), (x_cor, SCREEN_HEIGHT), 1)
        # Horizontal lines
        for num, i in enumerate(range(y_boxes)):
            y_cor = SCREEN_HEIGHT / y_boxes * i
            if num == 5: # Draw red line representing outer zone
                pygame.draw.line(surface, COLORS["RED"], (0, y_cor), (SCREEN_WIDTH, y_cor), 1)
            else:
                pygame.draw.line(surface, COLORS["WHITE"], (0, y_cor), (SCREEN_WIDTH, y_cor), 1)

    def print_board(self, pygame, surface, object = None):
        """
        Method managing printing process
        :param pygame: Pygame instance
        :param surface: Surface instance
        :param object: object to be printed
        :return: None
        """
        surface.fill(COLORS["BLACK"]) #Reset surface to black color
        self.print_edges(pygame, surface)
        if object is not None:
            object.print(self.board, pygame, surface)

        self.print_lines(pygame, surface)

        # Update the display
        pygame.display.flip()


    def is_collision(self, positions) -> bool:
        """
        Method to check if collision happened
        :param positions: position of the object
        :return: bool
        """
        for coord in positions:
            if not self.board[coord[1]][coord[0]].is_accessible():
                return True
        return False

    def create_object(self):
        """
        Method to create the object
        :return: None
        """
        chosen_object = random.choice(object_list) # Pick random object of the list
        new_object = chosen_object() # Make an instance of the object

        new_object.set_pos() # Set position of the object on the board

        if not self.is_collision(new_object.pos):
            return True, new_object
        else:
            return False, new_object


    def move_object(self, object, move : str) -> bool:
        """
        Method to move the object
        :param object: Object instance
        :param move: Move type
        :return: bool - success of the move
        """
        if move == "LEFT":
            new_pos = []
            new_center_pos = (object.center_pos[0] - 1, object.center_pos[1])
            for x, y in object.pos:
                new_pos.append((x - 1, y))

            if not self.is_collision(new_pos): # Set new values if no collision
                object.pos = new_pos
                object.center_pos = new_center_pos
                return True
            else:
                return False

        elif move == "RIGHT":
            new_pos = []
            new_center_pos = (object.center_pos[0] + 1, object.center_pos[1])
            for x, y in object.pos:
                new_pos.append((x + 1, y))

            if not self.is_collision(new_pos): # Set new values if no collision
                object.pos = new_pos
                object.center_pos = new_center_pos
                return True
            else:
                return False

        elif move == "DOWN":
            new_pos = []
            new_center_pos = (object.center_pos[0], object.center_pos[1] + 1)
            for x, y in object.pos:
                new_pos.append((x, y + 1))

            if not self.is_collision(new_pos): # Set new values if no collision
                object.pos = new_pos
                object.center_pos = new_center_pos
                return True
            else:
                return False

        else:
            raise ValueError(f"Bad move side {move}")

    def rotate_piece(self, object, move) -> bool:
        """
        Method to rotate the object
        :param object: Object instance
        :param move: Move type
        :return: bool - success of the move
        """
        if move == "LEFT":
            new_pos = []
            new_center_pos = (None, None)
            for x, y in object.pos:
                # Formula for the left rotation
                x2 = y + object.center_pos[0] - object.center_pos[1]
                y2 = object.center_pos[0] + object.center_pos[1] - x
                new_pos.append((x2, y2))
                if (x,y) == object.center_pos:
                    new_center_pos = (x2, y2)

            if not self.is_collision(new_pos): # Set new values if no collision
                object.pos = new_pos
                object.center_pos = new_center_pos
                return True
            else:
                return False

        elif move == "RIGHT":
            new_pos = []
            new_center_pos = (None, None)
            for x, y in object.pos:
                # Formula for the right rotation
                x2 = object.center_pos[0] + object.center_pos[1] - y
                y2 = x + object.center_pos[1] - object.center_pos[0]
                new_pos.append((x2, y2))
                if (x,y) == object.center_pos:
                    new_center_pos = (x2, y2)

            if not self.is_collision(new_pos): # Set new values if no collision
                object.pos = new_pos
                object.center_pos = new_center_pos
                return True
            else:
                return False

    def lock_object(self, object):
        """
        Method to lock the object and secure it on the board
        :param object: Object instance
        :return: None
        """
        for x, y in object.pos:
            self.board[y][x].set_accessible(False)
            self.board[y][x].set_color(object.color)

    def clear_lines(self, pygame, surface):
        """
        Method to clear the lines of the game board
        :param pygame: Pygame instance
        :param surface: Surface instance
        :return: None
        """
        try:
            reward = 0
            for y in range(1, y_boxes - 1): # Skip checking edges

                if all(not self.board[y][x].is_accessible() for x in range(1, x_boxes - 1)):
                    # Clear the row
                    reward += 5
                    for x in range(1, x_boxes - 1):
                        self.board[y][x].set_accessible(True)
                        self.board[y][x].set_color("BLACK")

                    #Drop above boxes after cleaning of the line
                    for above_y in reversed(range(1, y)):
                        for x in range(1, x_boxes - 1):
                            if self.board[above_y + 1][x].is_accessible():
                                self.board[above_y + 1][x].set_accessible(self.board[above_y][x].is_accessible())
                                self.board[above_y + 1][x].set_color(self.board[above_y][x].color)
                                self.board[above_y][x].set_color("BLACK")
                                self.board[above_y][x].set_accessible(True)


                    # Print after each line clearance
                    self.print_board(pygame, surface)
                    time.sleep(1)

            return reward


        except Exception as e:
            print(f"Error in clear line: {e}")

    def is_out(self) -> bool:
        """
        Method to check if the object is out of the game zone
        :return: bool
        """
        for x in range(1, x_boxes - 1):
            if not self.board[4][x].is_accessible():
                return True

        return False

    def is_at_bottom(self, object) -> bool:
        """
        Method checking if the object is at the bottom of the board and can be fixed
        :param object: Object to be fixed
        :return: Bool
        """
        new_pos = []
        for x, y in object.pos:
            new_pos.append((x, y + 1))

        if self.is_collision(new_pos):  # Set new values if no collision
            return True
        else:
            return False

    def apply_action(self, new_object, actions, pygame, surface):
        """
        Method to apply the action to the object
        :param new_object: Object to be moved
        :param actions: Action list to be done
        :param pygame: Pygame instance
        :param surface: Surface instance
        :return: reward, new_object_needed, output_action
        """
        for action in actions:
            if action == 0: # Move LEFT
                if not self.move_object(new_object, "LEFT"):
                    continue
                if self.is_at_bottom(new_object):
                    self.lock_object(new_object)  # Lock object on the board
                    reward, log_reward = self.get_reward(new_object, pygame, surface)
                    return reward, True, action, log_reward

            elif action == 1: # Move RIGHT
                if not self.move_object(new_object, "RIGHT"):
                    continue
                if self.is_at_bottom(new_object):
                    self.lock_object(new_object)  # Lock object on the board
                    reward, log_reward = self.get_reward(new_object, pygame, surface)
                    return reward, True, action, log_reward

            elif action == 2: # Move DOWN
                if not self.move_object(new_object, "DOWN"):
                    continue
                if self.is_at_bottom(new_object):
                    self.lock_object(new_object)  # Lock object on the board
                    reward, log_reward = self.get_reward(new_object, pygame, surface)
                    return reward, True, action, log_reward

            elif action == 3: # Rotate RIGHT
                if not self.rotate_piece(new_object, "RIGHT"):
                    continue
                if self.is_at_bottom(new_object):
                    self.lock_object(new_object)  # Lock object on the board
                    reward, log_reward = self.get_reward(new_object, pygame, surface)
                    return reward, True, action, log_reward

            elif action == 4: # Rotate LEFT
                if not self.rotate_piece(new_object, "LEFT"):
                    continue
                if self.is_at_bottom(new_object):
                    self.lock_object(new_object)  # Lock object on the board
                    reward, log_reward = self.get_reward(new_object, pygame, surface)
                    return reward, True, action, log_reward

            return 0, False, action, (0,0,0,0,0,0,0)

    def get_reward(self, object, pygame, surface):
        """
        Method to collect the rewards
        :param object: Current object
        :param pygame: Pygame instance
        :param surface: Surface instance
        :return: Reward sum, log output for rewards
        """
        reward_lines = self.clear_lines(pygame, surface)
        reward_gaps = self.check_gaps(object)
        reward_height = self.check_height(object)
        reward_tightness = self.check_tightness(object)
        reward_closeness = self.check_closeness(object)
        reward_centering = self.check_centering(object)
        reward_coverage = self.check_coverage()
        log_reward = (reward_lines, reward_gaps, reward_height, reward_tightness, reward_closeness,
                      reward_centering, reward_coverage)
        sum_reward = sum(log_reward)
        return sum_reward, log_reward

    def check_gaps(self, object):
        """
        Reward method checking if under the object are any gaps
        :param object: Current object
        :return: Reward
        """
        reward = 0
        y_max, x_list = object.get_ymax_coord()

        for x in x_list:
            if self.board[y_max + 1][x].is_accessible():
                reward -= 0.2 # Negative reward for every gap under the block

        if reward == 0: # If no gap return positive reward
            reward = 0.1

        return reward

    def check_height(self, object):
        """
        Reward method checking if in which height the block was placed, the lower the better
        :param object: Current object
        :return: Reward
        """
        reward = 0
        y_max, _ = object.get_ymax_coord()
        y_real = y_max - 1 - 4

        normalized_height = y_real / (y_boxes - 2 - 4)
        reward += 1.0 * normalized_height

        return reward

    def check_tightness(self, object):
        """
        Reward method checking if the bottom part of the block is placed tightly between oder blocks
        :param object: Current object
        :return: Reward
        """
        reward = 0
        y_max, x_list = object.get_ymax_coord()

        if (not self.board[y_max][x_list[0] - 1].is_accessible() and
                not self.board[y_max][x_list[len(x_list) - 1] + 1].is_accessible()):
            reward += 0.2 # Reward if it touches something on the left and right side

        return reward

    def check_centering(self, object):
        """
        Penalize blocks too far from the center
        :param object: Current object
        :return: Reward
        """
        reward = 0
        _, x_list = object.get_ymax_coord()
        board_center = x_boxes // 2
        for x in x_list:
            reward -= 0.1 * abs(x - board_center)  # Tweak weight
        return reward

    def check_closeness(self, object):
        """
        Reward method checking how far away are the closest blocks
        :param object: Current object
        :return: Reward
        """
        reward = 0
        heights = self.get_column_heights()
        std_dev = np.std(heights)
        mean_height = np.mean(heights)

        reward -= std_dev * 0.4  # penalty for uneven surfaces
        reward -= mean_height * 0.2 # penalty for stacking too high
        return reward

    def check_coverage(self):
        """
        Reward more filled columns
        :return: Reward
        """
        heights = self.get_column_heights()
        filled_columns = sum(1 for h in heights if h > 0)
        return filled_columns * 0.05

    def get_column_heights(self):
        """
        Method to get the heights of each column
        :return: List of heights
        """
        height_list = []
        for x in range(1, x_boxes - 1):
            height = 0
            for y in range(1, y_boxes - 1):
                if not self.board[y][x].is_accessible():
                    height += 1
            height_list.append(height)

        return height_list