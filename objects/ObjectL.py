from objects.Object import Object


class ObjectL(Object):
    def __init__(self):
        super().__init__()
        self.color = "ORANGE"
        for i in range(3):
            self.structure[i][1] = True
        self.structure[2][2] = True

