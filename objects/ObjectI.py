from objects.Object import Object


class ObjectI(Object):
    def __init__(self):
        for i in range(4):
            self.structure[i][1] = True

    def print(self):
        pass