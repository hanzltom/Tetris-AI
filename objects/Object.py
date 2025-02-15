import abc
from abc import ABC,  abstractstaticmethod
from screen_setup import SCREEN_WIDTH, SCREEN_HEIGHT, x_boxes, y_boxes


class Object(ABC):
    structure = [[ False for j in range(3)] for i in range(4)]
    pos = []
    center_pos = (None, None)
    color = None

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


