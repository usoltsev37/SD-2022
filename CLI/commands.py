from abc import ABC, abstractmethod
from os import getcwd
from typing import List
import subprocess


class Command(ABC):
    """Abstract class command. Each command is inherited from this class"""
    @abstractmethod
    def __init__(self, args: list):
        self.stdout = None
        self.stdin = None

    @abstractmethod
    def execute(self, stdin, stdout):
        pass


class Cat(Command):
    """Class which represents cat command"""
    def __init__(self, args: list):
        self.arg = args[0] if len(args) > 0 else None

    def cat_file(self, filename: str):
        try:
            with open(filename) as lines:
                for line in lines:
                    print(line, file=self.stdout, end='')
        except FileNotFoundError:
            print(f'cat: {filename}: No such file or directory')

    def execute(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        if not self.arg:
            self.cat_file(self.stdin.read().strip())
        else:
            self.cat_file(self.arg)


class Echo(Command):
    """Class which represents echo command"""
    def __init__(self, args: List[str]):
        self.args = args

    def execute(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        if len(self.args) != 0:
            print(*self.args, file=self.stdout, end='')
        else:
            print(self.stdin.read(), file=self.stdout, end='')


class Wc(Command):
    """Class which represents wc command"""
    def __init__(self, args):
        self.arg = args[0] if len(args) > 0 else None

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
        except FileNotFoundError:
            print(f'wc: {filename}: No such file or directory')

    def execute(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        if not self.arg:
            self.wc(self.stdin)
        else:
            self.wc_file(self.arg)


class Pwd(Command):
    """Class which represents pwd command"""
    def __init__(self, args):
        pass

    def execute(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        print(getcwd(), file=self.stdout)


class Exit(Command):
    """Class which represents exit command"""
    def __init__(self, args):
        pass

    def execute(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        raise SystemExit("CLI exit")


class Declaration(Command):
    """Class which represents declaration command"""
    def __init__(self, args):
        self.dct = args[0]
        self.name = args[1]
        self.value = args[2]

    def execute(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        self.dct[self.name] = self.value


class External(Command):
    """Class which represents external command"""
    def __init__(self, command, args):
        self.command = command
        self.args = args

    def execute(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        return subprocess.call([self.command, self.args], stdin=self.stdin, stdout=self.stdout)
