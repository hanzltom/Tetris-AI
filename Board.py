from screen_setup import SCREEN_WIDTH, SCREEN_HEIGHT, x_boxes, y_boxes
from Field import Field
from Position import Position

class Board:
    def __init__(self):
        self.board = [[]]

        for x in range(x_boxes):
            for y in range(y_boxes):

                x_cor = SCREEN_WIDTH / 11 * x
                y_cor = SCREEN_HEIGHT / 21 * y

                if x == 0 or x == 10 or y == 0 or y == 20:
                    self.board[x].append(
                        Field(Position(x_cor, y_cor, x_cor + SCREEN_WIDTH / 11, y_cor + SCREEN_HEIGHT / 21), False))
                self.board[x].append(Field(Position(x_cor, y_cor, x_cor + SCREEN_WIDTH / 11, y_cor + SCREEN_HEIGHT / 21)))

                #if i == 0 or i == 10:
                #    pygame.draw.rect(surface, COLORS["GREY"],
                #                     pygame.Rect(x_cor, y_cor, x_cor + SCREEN_WIDTH / 11, y_cor + SCREEN_HEIGHT / 21))
                #elif j == 0 or j == 20:
                #    pygame.draw.rect(surface, COLORS["GREY"],
                 #                    pygame.Rect(x_cor, y_cor, x_cor + SCREEN_WIDTH / 11, y_cor + SCREEN_HEIGHT / 21))