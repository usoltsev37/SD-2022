import io

from CLI.main import CLI
from CLI.commands import Echo, Cat, Wc, Pwd, Exit
from CLI.token_types import Token, Type


def test_cat():
    cli = CLI()
    tokens = [Token("cat", Type.STRING), Token("main.py", Type.STRING), Token(chr(0), Type.END)]
    cli.parseCommand(tokens) == Cat("main.py")


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
    tokens = [Token("wc", Type.STRING), Token("main.py", Type.STRING), Token(chr(0), Type.END)]
    cli.parseCommand(tokens) == Wc("main.py")


def test_pwd():
    cli = CLI()
    tokens = [Token("pwd", Type.STRING), Token(chr(0), Type.END)]
    cli.parseCommand(tokens) == Pwd([])


def test_exit():
    cli = CLI()
    tokens = [Token("exit", Type.STRING), Token(chr(0), Type.END)]
    cli.parseCommand(tokens) == Exit([])
