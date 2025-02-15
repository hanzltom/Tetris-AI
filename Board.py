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

object_list = [ObjectI, ObjectJ, ObjectL, ObjectO, ObjectS, ObjectT, ObjectZ]

class Board:
    def __init__(self):
        self.board = [[]]

        for y in range(y_boxes):
            self.board.append([])
            for x in range(x_boxes):

                x_cor = SCREEN_WIDTH / 11 * x
                y_cor = SCREEN_HEIGHT / 21 * y

                if x == 0 or x == 10 or y == 0 or y == 20:
                    self.board[y].append(
                        Field(Position( x, y, (x_cor, y_cor), (SCREEN_WIDTH / 11, SCREEN_HEIGHT / 21)), False))
                else:
                    self.board[y].append(
                    Field(Position( x, y, (x_cor, y_cor), (SCREEN_WIDTH / 11, SCREEN_HEIGHT / 21)), True))


    def print_edges(self, pygame, screen):
        [self.board[y][x].print(pygame, screen) for y in range(y_boxes) for x in range(x_boxes)]

    def print_lines(self, pygame, surface):
        # Vertical lines
        for i in range(x_boxes):
            x_cor = SCREEN_WIDTH / 11 * i
            pygame.draw.line(surface, COLORS["WHITE"], (x_cor, 0), (x_cor, SCREEN_HEIGHT), 1)
        # Horizontal lines
        for i in range(y_boxes):
            y_cor = SCREEN_HEIGHT / 21 * i
            pygame.draw.line(surface, COLORS["WHITE"], (0, y_cor), (SCREEN_WIDTH, y_cor), 1)

    def first_print(self, pygame, surface):
        surface.fill(COLORS["BLACK"])
        self.print_edges(pygame, surface)
        self.print_lines(pygame, surface)


    def is_collision(self, positions):
        for coord in positions:
            if not self.board[coord[1]][coord[0]].is_accessible():
                return True

    def create_object(self):
        chosen_object = random.choice(object_list)
        new_object = chosen_object()
        print(f"Vybrano: {type(new_object)}")
        new_object.set_pos()
        print(f"Pozice: {new_object.pos}")
        if not self.is_collision(new_object.pos):
            return True, new_object
        else:
            return False, new_object


    def move_object(self, object, move : str) -> bool:
        if move == "LEFT":
            new_pos = []
            new_center_pos = (object.center_pos[0] - 1, object.center_pos[1])
            for x, y in object.pos:
                new_pos.append((x - 1, y))

            if not self.is_collision(new_pos):
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

            if not self.is_collision(new_pos):
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

            if not self.is_collision(new_pos):
                object.pos = new_pos
                object.center_pos = new_center_pos
                return True
            else:
                return False

        else:
            raise ValueError(f"Bad move side {move}")

    def rotate_piece(self, object, move) -> bool:
        if move == "LEFT":
            new_pos = []
            new_center_pos = (None, None)
            for x, y in object.pos:
                x2 = y + object.center_pos[0] - object.center_pos[1]
                y2 = object.center_pos[0] + object.center_pos[1] - x
                new_pos.append((x2, y2))
                if (x,y) == object.center_pos:
                    new_center_pos = (x2, y2)

            if not self.is_collision(new_pos):
                object.pos = new_pos
                object.center_pos = new_center_pos
                return True
            else:
                return False

        elif move == "RIGHT":
            new_pos = []
            new_center_pos = (None, None)
            for x, y in object.pos:
                x2 = object.center_pos[0] + object.center_pos[1] - y
                y2 = x + object.center_pos[1] - object.center_pos[0]
                new_pos.append((x2, y2))
                if (x,y) == object.center_pos:
                    new_center_pos = (x2, y2)

            if not self.is_collision(new_pos):
                object.pos = new_pos
                object.center_pos = new_center_pos
                return True
            else:
                return False

    def lock_piece(self, object):
        for x, y in object.pos:
            self.board[y][x].accessible = False
            self.board[y][x].color = object.color

    def clear_lines(self, pygame, surface):
        try:
            for y in range(1, y_boxes - 1): # Skip checking edges

                if all(not self.board[y][x].is_accessible() for x in range(1, x_boxes - 1)):
                    # Clear the row
                    for x in range(1, x_boxes - 1):
                        self.board[y][x].accessible = True
                        self.board[y][x].color = "BLACK"

                    for above_y in reversed(range(1, y)):
                        for x in range(1, x_boxes - 1):
                            if self.board[above_y + 1][x].is_accessible():
                                self.board[above_y + 1][x].accessible = self.board[above_y][x].accessible
                                self.board[above_y + 1][x].color = self.board[above_y][x].color
                                self.board[above_y][x].color = "BLACK"
                                self.board[above_y][x].accessible = True


                    self.first_print(pygame, surface)
                    pygame.display.flip()
                    time.sleep(1)


        except Exception as e:
            print(f"Error in clear line: {e}")