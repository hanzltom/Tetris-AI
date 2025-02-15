class Position:
    """
    Class which serves as a Position with both coordinates for Fields
    """
    def __init__(self, x : int, y : int, start_coordinates : tuple, end_coordinates : tuple):
        # Coordinates in the matrice
        self.x = x
        self.y = y

        # Coordinates for printing on the board
        self.start_coordinates = start_coordinates
        self.end_coordinates = end_coordinates # Distance from the start coordinates