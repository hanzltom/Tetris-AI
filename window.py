import pygame
import sys

# Initialize Pygame
pygame.init()

def draw_board():
    # Vertical lines
    for i in range(11):
        x_cor = SCREEN_WIDTH / 11 * i
        pygame.draw.line(screen, WHITE, (x_cor, 0), (x_cor, SCREEN_HEIGHT), 1)
    # Horizontal lines
    for i in range(21):
        y_cor = SCREEN_HEIGHT / 21 * i
        pygame.draw.line(screen, WHITE, (0, y_cor), (SCREEN_WIDTH, y_cor), 1)

# Set up the window
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(BLACK)
    draw_board()
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
