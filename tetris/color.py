from enum import Enum


class Color(Enum):
    Black = -1
    Transparent = 0
    Red = 1
    Blue = 2
    Green = 3
    Orange = 4
    Cyan = 5
    Purple = 6
    Yellow = 7

    def __add__(self, __o: object) -> object:
        if __o is None:
            return self
        elif isinstance(__o, self.__class__):
            if self == self.__class__.Transparent:
                return __o
            elif __o == self.__class__.Transparent:
                return self
            else:
                return Color.Black
        else:
            raise NotImplementedError

    def __radd__(self, __o: object) -> object:
        return self + __o

    def __mul__(self, __o: object) -> object:
        if __o is None:
            return None
        elif isinstance(__o, bool):
            return self if __o else self.__class__.Transparent
        else:
            raise NotImplementedError

    def __rmul__(self, __o: object) -> object:
        return self * __o

    def __repr__(self) -> str:
        return self.name
