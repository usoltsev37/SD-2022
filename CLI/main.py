import sys
import io
from CLI.parser import Parser
from CLI.token_types import Token, Type
from CLI.commands import Command
import CLI.commands as commands
import re


class CLI:
    def __init__(self):
        self.vars = {}

    def substitution(self, token):
        if token.type == Type.SUBSTITUTION:
            print(self.vars.get(token.value, ''))
            return Token(self.vars.get(token.value, ''), Type.CLEAN_STRING)
        elif token.type == Type.STRING:
            new_str = ''
            pattern = re.compile(r'\$[a-zA-Z_][\w]*')
            pos = 0
            while True:
                match = pattern.search(token.value, pos)
                if match is not None:
                    new_str += token.value[pos:match.span()[0]]
                    pos = match.span()[1]
                    var_name = match.group(0)[1:]
                    new_str += self.vars.get(var_name, '')
                else:
                    break
            new_str += token.value[pos:]
            return Token(new_str, Type.CLEAN_STRING)
        else:
            return token

    def parseCommand(self, tokens) -> Command:
        d = {
            'cat': commands.Cat,
            'echo': commands.Echo,
            'wc': commands.Wc,
            'pwd': commands.Pwd,
            'exit': commands.Exit
        }
        com_name = tokens[0].value
        args = [i.value for i in tokens[1:]]
        if com_name not in d:
            return commands.External(com_name, [self.vars] + args)
        else:
            return d[com_name](args)

    def process(self, line: str, stdin, stdout):
        parser = Parser(line)
        tokens = [self.substitution(t) for t in parser.parse()]
        io_in = stdin
        io_out = io.StringIO()
        pos = 0
        if pos == 0 and tokens[pos + 1].type == Type.DECLARATION:
            command = commands.Declaration([self.vars, tokens[pos], tokens[pos + 2]])
            command.execute(io_in, io_out)
            io_in = io_out
            io_in.seek(0, 0)
            io_out = io.StringIO()
            pos += 3
        begin = pos
        while pos < len(tokens):
            if tokens[pos].type == Type.PIPE or tokens[pos].type == Type.END:
                if len(tokens[begin:pos]) > 0:
                    command = self.parseCommand(tokens[begin:pos])
                    command.execute(io_in, io_out)
                    io_in = io_out
                    io_in.seek(0, 0)
                    io_out = io.StringIO()
                    begin = pos + 1
            pos += 1
        stdout.write(io_in.read())
        stdout.write('\n')


if __name__ == '__main__':
    try:
        cli = CLI()
        print('> ', end='')
        for line in sys.stdin:
            line = line.rstrip('\n')
            cli.process(line, sys.stdin, sys.stdout)
            print('> ', end='')
    except SystemExit as exc:
        print("CLI exit")
