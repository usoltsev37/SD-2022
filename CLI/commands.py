from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout

    @abstractmethod
    def execute(self):
        pass


class Cat(Command):
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout

    def execute(self):
        pass


class Echo(Command):
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout

    def execute(self):
        pass


class Wc(Command):
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout

    def execute(self):
        pass


class Pwd(Command):
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout

    def execute(self):
        pass


class Exit(Command):
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout

    def execute(self):
        pass


class Declaration(Command):
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout

    def execute(self):
        pass


class External(Command):
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout

    def execute(self):
        pass
