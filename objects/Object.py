import abc
from abc import ABC,  abstractstaticmethod


class Object(ABC):
    structure = [[ False for j in range(3)] for i in range(4)]
    pos = []

    @abc.abstractmethod
    def print(self):
        pass