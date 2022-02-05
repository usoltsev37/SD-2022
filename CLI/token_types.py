from enum import Enum


class Type(Enum):
    STRING = 1
    CLEAN_STRING = 2
    SUBSTITUTION = 3
    DECLARATION = 4
    PIPE = 5
    END = 6


class Token:
    def __init__(self, value: str, token_type: Type):
        self.value = value
        self.type = token_type

    def getValue(self):
        return self.value

    def getType(self):
        return self.type

    def __repr__(self):
        return f'{self.type}({self.value})'
