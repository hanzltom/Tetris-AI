from Board import Board

class Game:
    def __init__(self, pygame, surface):
        self.board = Board()
        self.board.first_print(pygame, surface)

    def loop(self, pygame, surface):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update the display
            pygame.display.flip()