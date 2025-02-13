from abc import ABC,  abstractstaticmethod


class Object(ABC):
    structure = [[]]

    @abstractstaticmethod
    def print():
        pass