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
                    reward += 1
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
        new_pos = []
        for x, y in object.pos:
            new_pos.append((x, y + 1))

        if self.is_collision(new_pos):  # Set new values if no collision
            return True
        else:
            return False

    def apply_action(self, new_object, action, pygame, surface):
        if action == 0:
            self.move_object(new_object, "LEFT")
            if self.is_at_bottom(new_object):
                self.lock_object(new_object)  # Lock object on the board
                reward_lines = self.clear_lines(pygame, surface)
                reward_lines *= 20
                _, reward_depth = new_object.center_pos
                reward = reward_lines + reward_depth - 1
                return reward, True

        elif action == 1:
            self.move_object(new_object, "RIGHT")
            if self.is_at_bottom(new_object):
                self.lock_object(new_object)  # Lock object on the board
                reward_lines = self.clear_lines(pygame, surface)
                reward_lines *= 20
                _, reward_depth = new_object.center_pos
                reward = reward_lines + reward_depth - 1
                return reward, True

        elif action == 2:
            self.move_object(new_object, "DOWN")
            if self.is_at_bottom(new_object):
                self.lock_object(new_object)  # Lock object on the board
                reward_lines = self.clear_lines(pygame, surface)
                reward_lines *= 20
                _, reward_depth = new_object.center_pos
                reward = reward_lines + reward_depth - 1
                return reward, True

        elif action == 3:
            self.rotate_piece(new_object, "RIGHT")
            if self.is_at_bottom(new_object):
                self.lock_object(new_object)  # Lock object on the board
                reward_lines = self.clear_lines(pygame, surface)
                reward_lines *= 20
                _, reward_depth = new_object.center_pos
                reward = reward_lines + reward_depth - 1
                return reward, True

        elif action == 4:
            self.rotate_piece(new_object, "LEFT")
            if self.is_at_bottom(new_object):
                self.lock_object(new_object)  # Lock object on the board
                reward_lines = self.clear_lines(pygame, surface)
                reward_lines *= 20
                _, reward_depth = new_object.center_pos
                reward = reward_lines + reward_depth - 1
                return reward, True

        return 0, False