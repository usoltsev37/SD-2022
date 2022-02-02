from abc import ABC, abstractmethod
from os import getcwd
from typing import List


class Command(ABC):
    @abstractmethod
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout

    @abstractmethod
    def execute(self):
        pass


class Cat(Command):
    def __init__(self, stdin, stdout, arg: str):
        self.stdin = stdin
        self.stdout = stdout
        self.arg = arg

    def cat(self, lines):
        for line in lines:
            print(line, file=self.stdout, end='')

    def cat_file(self, filename: str):
        try:
            with open(filename) as file:
                self.cat(file)
        except:
            print(f'cat: {filename}: No such file or directory')

    def execute(self):
        if not self.arg:
            self.cat(self.stdin)
        else:
            self.cat_file(self.arg)


class Echo(Command):
    def __init__(self, stdin, stdout, args: List[str]):
        self.stdin = stdin
        self.stdout = stdout
        self.args = args

    def execute(self):
        print(*self.args, file=self.stdout)


class Wc(Command):
    def __init__(self, stdin, stdout, arg):
        self.stdin = stdin
        self.stdout = stdout
        self.arg = arg

    def wc(self, lines):
        lines_cnt = 0
        words_cnt = 0
        bytes_cnt = 0
        for line in lines:
            lines_cnt += 1
            words_cnt += len(line.split())
            bytes_cnt += len(line.encode("utf-8"))
        return lines_cnt, words_cnt, bytes_cnt

    def wc_file(self, filename):
        try:
            with open(filename) as file:
                result = self.wc(file)
                print(*result, filename, file=self.stdout)
        except:
            print(f'wc: {filename}: No such file or directory')

    def execute(self):
        if not self.arg:
            self.wc(self.stdin)
        else:
            self.wc_file(self.arg)


class Pwd(Command):
    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout

    def execute(self):
        print(getcwd(), file=self.stdout)


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
