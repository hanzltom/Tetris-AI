from objects.Object import Object


class ObjectO(Object):
    def __init__(self):
        super().__init__()
        self.color = "YELLOW"
        self.structure[0][0] = True
        self.structure[0][1] = True
        self.structure[1][0] = True
        self.structure[1][1] = True

