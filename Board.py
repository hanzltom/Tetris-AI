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

    def is_collision(self, new_object):
        for coord in new_object.pos:
            if not self.board[coord[1]][coord[0]].is_accessible():
                return True

    def create_object(self):
        chosen_object = random.choice(object_list)
        new_object = chosen_object()
        print(f"Vybrano: {type(new_object)}")
        new_object.set_pos()
        print(f"Pozice: {new_object.pos}")
        if not self.is_collision(new_object):
            return True, new_object
        else:
            return False, new_object


    def move_object(self, object, move : str) -> bool:
        if move == "LEFT":
            for x, y in object.pos:
                if not self.board[y][x - 1].is_accessible():
                    return False

            new_pos = []
            object.center_pos = (object.center_pos[0] - 1, object.center_pos[1])
            for x, y in object.pos:
                new_pos.append((x - 1, y))

            object.pos = new_pos
            return True

        elif move == "RIGHT":
            for x, y in object.pos:
                if not self.board[y][x + 1].is_accessible():
                    return False

            new_pos = []
            object.center_pos = (object.center_pos[0] + 1, object.center_pos[1])
            for x, y in object.pos:
                new_pos.append((x + 1, y))

            object.pos = new_pos
            return True

        elif move == "DOWN":
            for x, y in object.pos:
                if not self.board[y + 1][x].is_accessible():
                    return False

            new_pos = []
            object.center_pos = (object.center_pos[0], object.center_pos[1] + 1)
            for x, y in object.pos:
                new_pos.append((x, y + 1))

            object.pos = new_pos
            return True

        else:
            raise ValueError(f"Bad move {move}")

    def rotate_piece(self, object, move):
        if move == "LEFT":
            new_pos = []
            for x, y in object.pos:
                x2 = y +
                y2 =
        elif move == "RIGHT":
            pass
        else:
            raise ValueError(f"Bad move {move}")