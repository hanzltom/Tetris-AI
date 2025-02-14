from objects.Object import Object


class ObjectZ(Object):
    def __init__(self):
        self.color = "GREEN"
        self.structure[0][0] = True
        self.structure[0][1] = True
        self.structure[1][1] = True
        self.structure[1][2] = True

