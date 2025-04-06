import abc
from abc import ABC,  abstractstaticmethod
from screen_setup import SCREEN_WIDTH, SCREEN_HEIGHT, x_boxes, y_boxes


class Object(ABC):
    def __init__(self):
        self.structure = [[False for j in range(3)] for i in range(4)]
        self.pos = []
        self.center_pos = (None, None)
        self.color = None

    def print(self, board, pygame, surface):
        for x, y in self.pos:
            board[y][x].print_object(pygame, surface, self.color)

    def set_pos(self):
        start_x = x_boxes // 2 - 1
        for y in range(4):
            for x in range(3):
                if self.structure[y][x]:
                    self.pos.append((start_x + x, y + 1))

        self.center_pos = (start_x + 1, 2)

    def get_ymax_coord(self):
        y_max = 0
        x_list = []
        for x, y in self.pos:
            if y > y_max:
                x_list.clear()
                y_max = y
            if y == y_max:
                x_list.append(x)

        return y_max, x_list


