from CLI.parser import Parser
from CLI.token_types import Type, Token


def test_parse_cat():
    line = "cat main.py"
    parser = Parser(line)
    expected_result = [Token("cat", Type.STRING), Token("main.py", Type.STRING), Token(chr(0), Type.END)]
    assert parser.parse() == expected_result


def test_parse_echo_one_argument():
    line = "echo 1"
    parser = Parser(line)
    expected_result = [Token("echo", Type.STRING), Token("1", Type.STRING), Token(chr(0), Type.END)]
    assert parser.parse() == expected_result


def test_parse_echo_many_arguments():
    line = "echo 1 2 3"
    parser = Parser(line)
    expected_result = [Token("echo", Type.STRING), Token("1", Type.STRING), Token("2", Type.STRING),
                       Token("3", Type.STRING), Token(chr(0), Type.END)]
    assert parser.parse() == expected_result


def test_parce_wc():
    line = "wc file.txt"
    parser = Parser(line)
    expected_result = [Token("wc", Type.STRING), Token("file.txt", Type.STRING), Token(chr(0), Type.END)]
    assert parser.parse() == expected_result


def test_parse_pwd():
    line = "pwd"
    parser = Parser(line)
    expected_result = [Token("pwd", Type.STRING), Token(chr(0), Type.END)]
    assert parser.parse() == expected_result


def test_parse_exit():
    line = "exit"
    parser = Parser(line)
    expected_result = [Token("exit", Type.STRING), Token(chr(0), Type.END)]
    assert parser.parse() == expected_result


def test_parse_quotes_echo_one_word():
    line = "echo 'Hello'"
    parser = Parser(line)
    expected_result = [Token("echo", Type.STRING), Token("Hello", Type.CLEAN_STRING), Token(chr(0), Type.END)]
    assert parser.parse() == expected_result


def test_parse_quotes_echo_many_words():
    line = "echo 'Hello world!'"
    parser = Parser(line)
    expected_result = [Token("echo", Type.STRING), Token("Hello world!", Type.CLEAN_STRING), Token(chr(0), Type.END)]
    assert parser.parse() == expected_result


def test_parse_quotes():
    line = 'cat "file.txt"'
    parser = Parser(line)
    expected_result = [Token("cat", Type.STRING), Token("file.txt", Type.STRING), Token(chr(0), Type.END)]
    assert parser.parse() == expected_result
