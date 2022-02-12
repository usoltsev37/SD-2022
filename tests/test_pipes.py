from CLI.commands import Cat, Echo, Wc, Exit
from CLI.main import CLI
import io

from CLI.parser import Parser
from CLI.token_types import Token, Type


def test_execute_pipes_echo_cat():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "echo Hello | cat"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "Hello\n"


def test_parse_pipes_echo_cat():
    line = "echo Hello | cat"
    parser = Parser(line, {})
    assert parser.parse() == [Echo(["Hello"]), Cat([])]


def test_parseCommands_pipes_echo_wc():
    line = "echo Hello | wc"
    parser = Parser(line, {})
    tokens = [Token("echo", Type.STRING), Token("Hello", Type.STRING), Token("|", Type.PIPE), Token("wc", Type.STRING),
              Token(chr(0), Type.END)]
    assert parser.parseCommands(tokens) == [Echo(["Hello"]), Wc([])]


def test_execute_pipes_with_exit_middle():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    assert cli.is_running == True
    line = "echo Hello | exit | echo world"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "world\n"
    assert cli.is_running == True


def test_execute_pipes_exit_end():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    assert cli.is_running == True
    line = "x=1 | echo $x | exit"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "\n"
    assert cli.is_running == True


def test_execute_pipes_with_vars():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "x=1 | echo $x"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "\n"

