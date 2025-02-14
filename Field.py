from Position import Position
from colors import COLORS

class Field:
    def __init__(self, pos : Position, accessible : bool = True):
        self.accessible = accessible
        self.color = "BLACK" if accessible else "GREY"
        self.pos = pos

    def is_accessible(self):
        return self.accessible

    def print(self, pygame, surface):
        pygame.draw.rect(surface, COLORS[self.color],
                         pygame.Rect(self.pos.start_coordinates, self.pos.end_coordinates))

    def print_object(self, pygame, surface, color):
        pygame.draw.rect(surface, COLORS[color],
                         pygame.Rect(self.pos.start_coordinates, self.pos.end_coordinates))