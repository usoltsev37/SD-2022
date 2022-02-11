import io

import pytest as pytest
from CLI.main import CLI
from CLI.commands import Echo, Cat, Wc, Pwd, Exit
from CLI.token_types import Token, Type


def test_cat():
    cli = CLI()
    tokens = [Token("cat", Type.STRING), Token("main.py", Type.STRING)]
    cli.parseCommand(tokens) == Cat(["main.py"])


def test_execute_cat():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "cat tests/file.txt"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "Hello world!\n"


def test_echo_one_argument():
    cli = CLI()
    tokens = [Token("echo", Type.STRING), Token("Hello", Type.STRING), Token(chr(0), Type.END)]
    cli.parseCommand(tokens) == Echo("Hello")


def test_echo_many_arguments():
    cli = CLI()
    tokens = [Token("echo", Type.STRING), Token("Hello", Type.STRING), Token("world", Type.STRING),
              Token(chr(0), Type.END)]
    cli.parseCommand(tokens) == Echo(["Hello", "world"])


def test_execute_echo():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "echo Hello"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "Hello\n"


def test_wc_file():
    cli = CLI()
    tokens = [Token("wc", Type.STRING), Token("main.py", Type.STRING)]
    cli.parseCommand(tokens) == Wc(["main.py"])


def test_execute_wc():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "wc tests/file.txt"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "1 2 12 tests/file.txt\n"


def test_pwd():
    cli = CLI()
    tokens = [Token("pwd", Type.STRING), Token(chr(0), Type.END)]
    cli.parseCommand(tokens) == Pwd([])


def test_exit():
    cli = CLI()
    tokens = [Token("exit", Type.STRING), Token(chr(0), Type.END)]
    cli.parseCommand(tokens) == Exit([])


def test_execute_exit():
    cli = CLI()
    assert cli.is_running == True
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "exit"
    cli.process(line, stdin, stdout)
    assert cli.is_running == False


def test_declaration():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "x=5"
    cli.process(line, stdin, stdout)
    line = "echo $x"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "5\n"
