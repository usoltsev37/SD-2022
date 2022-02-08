from abc import ABC, abstractmethod
from os import getcwd
from typing import List
import subprocess as sb


class Command(ABC):
    """Abstract class command. Each command is inherited from this class"""

    @abstractmethod
    def __init__(self, args: list):
        """
        Makes self.args same as given args
        :param args: list of command arguments
        """
        self.args = args

    @abstractmethod
    def execute(self, stdin, stdout):
        """
        Function executes command with the given arguments
        :param stdin: input stream
        :param stdout: ouput stream
        """
        pass


class Cat(Command):
    """Class which represents cat command"""

    def __init__(self, args: List[str]):
        """
        Makes self.args same as given args list
        :param args: list of command arguments
        :raise AttributeError if the length of the args list is greater than 1
        """
        if len(args) > 1:
            raise AttributeError("Too many arguments")
        self.arg = args[0] if len(args) > 0 else None

    def cat(self, lines):
        """
        Function that cat given lines
        :param lines: input lines
        :return: None
        """
        for line in lines:
            print(line, file=self.stdout, end='')

    def cat_file(self, filename: str):
        """
        Print the content of the given file into output stream
        :param filename: name of the file
        :raise FileNotFoundError if the given file cannot be found
        :return: None
        """
        try:
            with open(filename) as lines:
                self.cat(lines)
        except FileNotFoundError:
            print(f'cat: {filename}: No such file or directory')

    def execute(self, stdin, stdout):
        """
        Function executes cat command
        :param stdin: input stream
        :param stdout: output stream
        :return: None
        """
        self.stdin = stdin
        self.stdout = stdout
        if not self.arg:
            self.cat(self.stdin.read().strip())
        else:
            self.cat_file(self.arg)


class Echo(Command):
    """Class which represents echo command"""

    def __init__(self, args: List[str]):
        """
        Makes self.args same as given args list
        :param args: list of command arguments
        """
        self.args = args

    def execute(self, stdin, stdout):
        """
        Function executes echo command
        :param stdin: input stream
        :param stdout: output stream
        :return: None
        """
        if len(self.args) != 0:
            print(*self.args, file=stdout, end='')
        else:
            print(stdin.read(), file=stdout, end='')


class Wc(Command):
    """Class which represents wc command"""

    def __init__(self, args: List[str]):
        """
        Makes self.args same as given args list
        :param args: list of command arguments
        :raise AttributeError if the length of the args list is greater than 1
        """
        if len(args) > 1:
            raise AttributeError("Too many arguments")
        self.arg = args[0] if len(args) > 0 else None

    def wc(self, lines):
        """
        Function that calculates count of lines, words and bytes
        :param lines: lines which represents data with text
        :return: total number of lines, words and bytes in the given lines
        """
        lines_cnt = 0
        words_cnt = 0
        bytes_cnt = 0
        for line in lines:
            lines_cnt += 1
            words_cnt += len(line.split())
            bytes_cnt += len(line.encode("utf-8"))
        return lines_cnt, words_cnt, bytes_cnt

    def wc_file(self, filename: str):
        """
        Functuon that calculates total number of lines, words and bytes in the given file
        :param filename: name of the file
        :raise FileNotFoundError if the given file cannot be found
        :return: None
        """
        try:
            with open(filename) as file:
                result = self.wc(file)
                print(*result, filename, file=self.stdout, end='')
        except FileNotFoundError:
            print(f'wc: {filename}: No such file or directory')

    def execute(self, stdin, stdout):
        """
        Function executes wc command
        :param stdin: input stream
        :param stdout: output stream
        :return: None
        """
        self.stdin = stdin
        self.stdout = stdout
        if not self.arg:
            print(*self.wc(self.stdin), file=self.stdout, end='')
        else:
            self.wc_file(self.arg)


class Pwd(Command):
    """Class which represents pwd command"""

    def __init__(self, args):
        pass

    def execute(self, stdin, stdout):
        """
        Function executes pwd command
        :param stdin: input stream
        :param stdout: output stream
        :return: None
        """
        print(getcwd(), file=stdout, end='')


class Exit(Command):
    """Class which represents exit command"""

    def __init__(self, args):
        pass

    def execute(self, stdin, stdout):
        """
        Function executes exit command
        :param stdin: input stream
        :param stdout: output stream
        :raise SystemExit exception
        :return: None
        """
        raise SystemExit("CLI exit")


class Declaration(Command):
    """Class which represents declaration command"""

    def __init__(self, args):
        """
        Initialize of the dict, name and value of the variable
        :param args: [dict of variables, name, value]
        :raise AttributeError if the length of the args list is not equals to 3
        """
        if len(args) != 3:
            raise AttributeError("Declaration class needs 3 arguments")
        self.dct = args[0]
        self.name = args[1]
        self.value = args[2]

    def execute(self, stdin, stdout):
        """
        Function executes declaration command
        :param stdin: input stream
        :param stdout: output stream
        :return: None
        """
        self.dct[self.name] = self.value


class External(Command):
    """Class which represents external command"""

    def __init__(self, args: List[str]):
        """
        Initialize of the dict, name and value of the variable
        :param args: list of command arguments
        :raise AttributeError if the length of the args list is equals zero
        """
        if len(args) < 2:
            raise AttributeError("External: command and vars expected")
        self.command = args[0]
        self.vars = args[1]
        self.args = args[2:]

    def execute(self, stdin, stdout):
        """
        Function executes external command
        :param stdin: input stream
        :param stdout: output stream
        """
        if stdin.isatty():
            inp = stdin.read().encode()
        else:
            inp = b''
        proc = sb.run([self.command] + self.args, input=inp, stdout=sb.PIPE)
        print(proc.stdout.decode(), file=stdout, end='')
