from screen_setup import SCREEN_WIDTH, SCREEN_HEIGHT, x_boxes, y_boxes
from colors import COLORS

def draw_board(pygame, surface):
    # Vertical lines
    for i in range(x_boxes):
        x_cor = SCREEN_WIDTH / 11 * i
        pygame.draw.line(surface, COLORS["WHITE"], (x_cor, 0), (x_cor, SCREEN_HEIGHT), 1)
    # Horizontal lines
    for i in range(y_boxes):
        y_cor = SCREEN_HEIGHT / 21 * i
        pygame.draw.line(surface, COLORS["WHITE"], (0, y_cor), (SCREEN_WIDTH, y_cor), 1)

def draw_edges(pygame, surface):
    for i in range(x_boxes):
        for j in range(y_boxes):

            x_cor = SCREEN_WIDTH / 11 * i
            y_cor = SCREEN_HEIGHT / 21 * j
            if i == 0 or i == 10:
                pygame.draw.rect(surface, COLORS["GREY"], pygame.Rect(x_cor, y_cor,x_cor + SCREEN_WIDTH / 11, y_cor + SCREEN_HEIGHT / 21))
            elif j == 0 or j == 20:
                pygame.draw.rect(surface, COLORS["GREY"], pygame.Rect(x_cor, y_cor, x_cor + SCREEN_WIDTH / 11, y_cor + SCREEN_HEIGHT / 21))
