from Board import Board
from colors import COLORS
from screen_setup import *

class Game:
    def __init__(self, pygame, surface):
        self.board = Board()
        self.board.first_print(pygame, surface)
        pygame.display.flip()


    def loop(self, pygame, surface):
        try:
            input("Press Enter to continue")
            clock = pygame.time.Clock()  # To control the frame rate
            drop_interval = 500  # Time in milliseconds for automatic downward movement
            last_drop_time = pygame.time.get_ticks()
            running = True
            new_object = None
            create_new_object = True
            while running:
                current_time = pygame.time.get_ticks()

                if create_new_object:
                    create_new_object = False
                    print("Finding new object")
                    object_valid, new_object = self.board.create_object()
                    while not object_valid:
                        print("New object is invalid")
                        object_valid, new_object = self.board.create_object()
                        print("Valid object found")

                self.board.first_print(pygame, surface)
                new_object.print(self.board.board, pygame, surface)
                self.board.print_lines(pygame, surface)
                # Update the display
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.board.move_object(new_object, "LEFT")
                        elif event.key == pygame.K_d:
                            self.board.move_object(new_object, "RIGHT")
                        elif event.key == pygame.K_s:
                            self.board.move_object(new_object, "DOWN")
                        elif event.key == pygame.K_e:
                            self.board.rotate_piece(new_object, "RIGHT")
                        elif event.key == pygame.K_q:
                            self.board.rotate_piece(new_object, "LEFT")


                """if current_time - last_drop_time > drop_interval:
                    if not self.board.move_piece_down():  # Try to move piece down
                        self.board.lock_piece()  # Lock piece if it can't move
                        self.board.clear_lines()  # Clear completed lines
                        self.board.spawn_new_piece()  # Spawn a new piece
                    last_drop_time = current_time
                """

        except Exception as e:
            print(f"Error: {e}")

