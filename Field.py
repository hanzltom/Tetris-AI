from Position import Position

class Field:
    def __init__(self, pos : Position, accessible : bool = True):
        self.accessible = accessible
        self.color = "BLACK" if accessible else "GREY"
        self.pos = pos