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
            clock = pygame.time.Clock()  # To control the frame rate
            drop_interval = 1500  # Time in milliseconds for automatic downward movement
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
                            suc = self.board.move_object(new_object, "LEFT")
                            print(f"Move left {suc}")
                        elif event.key == pygame.K_d:
                            suc = self.board.move_object(new_object, "RIGHT")
                            print(f"Move right {suc}")
                        elif event.key == pygame.K_s:
                            suc = self.board.move_object(new_object, "DOWN")
                            print(f"Move down {suc}")
                        elif event.key == pygame.K_e:
                            suc = self.board.rotate_piece(new_object, "RIGHT")
                        elif event.key == pygame.K_q:
                            suc = self.board.rotate_piece(new_object, "LEFT")


                if current_time - last_drop_time > drop_interval:
                    if not self.board.move_object(new_object, "DOWN"):
                        self.board.lock_piece(new_object)
                        self.board.clear_lines(pygame, surface)
                        create_new_object = True
                    last_drop_time = current_time


        except Exception as e:
            print(f"Error: {e}")

