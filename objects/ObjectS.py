from objects.Object import Object


class ObjectS(Object):
    def __init__(self):
        self.color = "RED"
        self.structure[0][1] = True
        self.structure[0][2] = True
        self.structure[1][0] = True
        self.structure[1][1] = True

