from Position import Position
from colors import COLORS

class Field:
    """
    CLass Field representing one field in board matrice
    """
    def __init__(self, pos : Position, accessible : bool = True):
        """
        Constructor of Field
        :param pos: position of the field in the matrice
        :param accessible: if the field is accessible for the object
        """
        self.accessible = accessible
        self.color = "BLACK" if accessible else "GREY"
        self.pos = pos

    def is_accessible(self) -> bool:
        """
        Method to check if the field is accessible for the object
        :return: bool
        """
        return self.accessible

    def set_accessible(self, accessible: bool):
        """
        Method to set accessible for the Field
        :param accessible: New accessible value
        :return: None
        """
        self.accessible = accessible

    def set_color(self, color: str):
        """
        Method to set color for the Field
        :param color: New color value
        :return: None
        """
        self.color = color

    def print(self, pygame, surface):
        """
        Print method to print the Field on the board
        :param pygame: Pygame instance
        :param surface: Surface instance
        :return: None
        """
        pygame.draw.rect(surface, COLORS[self.color],
                         pygame.Rect(self.pos.start_coordinates, self.pos.end_coordinates))

    def print_object(self, pygame, surface, color):
        """
        Print method to print the Field on the object
        :param pygame: Pygame instance
        :param surface: Surface instance
        :param color: Color of the object
        :return: None
        """
        pygame.draw.rect(surface, COLORS[color],
                         pygame.Rect(self.pos.start_coordinates, self.pos.end_coordinates))