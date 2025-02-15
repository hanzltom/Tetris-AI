from objects.Object import Object


class ObjectT(Object):
    def __init__(self):
        super().__init__()
        self.color = "PURPLE"
        self.structure[0][0] = True
        self.structure[0][1] = True
        self.structure[0][2] = True
        self.structure[1][1] = True

