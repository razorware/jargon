from abc import ABC, \
    abstractmethod


class Operator(ABC):

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, value):
        self.__left = value

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, value):
        self.__right = value

    def __init__(self):
        self.__left = lambda x: True
        self.__right = lambda x: True

    @abstractmethod
    def execute(self, x):
        pass


class OrOp(Operator):

    def __init__(self):
        Operator.__init__(self)

    def execute(self, x):
        l = self.left if not isinstance(self.left, OrOp) else self.left.execute
        r = self.right if not isinstance(self.right, OrOp) else self.right.execute

        return l(x) or r(x)
