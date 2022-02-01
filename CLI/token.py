from enum import Enum


class Type(Enum):
    STRING = 1
    SUBSTITUTION = 2
    DECLARATION = 3
    PIPE = 3


class Token:

    def __init__(self, value: str, type: Type):
        self.value = value
        self.type = type

    def getValue(self):
        return self.value

    def getType(self):
        return self.type
