from objects.Object import Object


class ObjectJ(Object):
    def __init__(self):
        super().__init__()
        self.color = "PINK"
        for i in range(3):
            self.structure[i][1] = True
        self.structure[2][0] = True

