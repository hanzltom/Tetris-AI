from screen_setup import SCREEN_WIDTH, SCREEN_HEIGHT, x_boxes, y_boxes
from Field import Field
from Position import Position
from colors import COLORS

class Board:
    def __init__(self):
        self.board = [[]]

        for x in range(x_boxes):
            self.board.append([])
            for y in range(y_boxes):

                x_cor = SCREEN_WIDTH / 11 * x
                y_cor = SCREEN_HEIGHT / 21 * y

                if x == 0 or x == 10 or y == 0 or y == 20:
                    self.board[x].append(
                        Field(Position( x, y, (x_cor, y_cor), (x_cor + SCREEN_WIDTH / 11, y_cor + SCREEN_HEIGHT / 21)), False))
                else:
                    self.board[x].append(
                    Field(Position( x, y, (x_cor, y_cor), (x_cor + SCREEN_WIDTH / 11, y_cor + SCREEN_HEIGHT / 21)), True))


    def print(self, pygame, screen):
        [self.board[x][y].print(pygame, screen) for y in range(y_boxes) for x in range(x_boxes)]

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
        self.print(pygame, surface)
        self.print_lines(pygame, surface)