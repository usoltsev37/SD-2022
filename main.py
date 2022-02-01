import sys
from CLI.parser import Parser

if __name__ == '__main__':
    for line in sys.stdin:
        line = line.rstrip('\n')
        #  print(line)
        parser = Parser()
        tokens = parser.parse(line)
