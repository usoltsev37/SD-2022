import io
import os

from CLI.main import CLI


def test_execute_cat():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "cat tests/file.txt"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "Hello world!\n"


def test_execute_echo():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "echo Hello"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "Hello\n"


def test_execute_wc():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "wc tests/file.txt"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "1 2 12 tests/file.txt\n"


def test_execute_pwd():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "pwd"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == os.getcwd() + '\n'


def test_execute_exit():
    cli = CLI()
    assert cli.is_running == True
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "exit"
    cli.process(line, stdin, stdout)
    assert cli.is_running == False


def test_execute_external():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    assert os.path.exists('./external.txt') == False
    line = "touch ./external.txt"
    cli.process(line, stdin, stdout)
    assert os.path.exists('./external.txt') == True
    line = "rm ./external.txt"
    cli.process(line, stdin, stdout)
    assert os.path.exists('./external.txt') == False


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
    assert result == "\n5\n"


def test_declaration_twice():
    cli = CLI()
    stdin = io.StringIO()
    stdout = io.StringIO()
    line = "x=5"
    cli.process(line, stdin, stdout)
    line = "x=10"
    cli.process(line, stdin, stdout)
    line = "echo $x"
    cli.process(line, stdin, stdout)
    stdout.seek(0, 0)
    result = stdout.read()
    assert result == "\n\n10\n"
