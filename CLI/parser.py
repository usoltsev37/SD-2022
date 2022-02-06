from typing import List
from CLI.token_types import Type, Token
from collections import OrderedDict
import re


class Parser:
    """Class for parsing the string"""

    tokens = OrderedDict([
        (Type.PIPE, r'\|'),
        (Type.DECLARATION, r'='),
        (Type.SUBSTITUTION, r'\$[a-zA-Z_][\w\-]*'),
        (Type.CLEAN_STRING, r'\'[^\']*\''),
        (Type.STRING, r'(\"[^\"]*\")|([\w\-\.\!\@\?\#\$\%\^\&\*\(\)\-\+]+)'),
        (Type.END, chr(0))
    ])

    def __init__(self, string: str):
        """
        Parser Constructor
        :param string: line for parsing
        """
        self.string = string + chr(0)
        self.pos = 0
        self.n = len(self.string)

    def _skip_ws(self):
        """Private. Skips leading spaces.
        :return:None
        """
        while self.pos < self.n and self.string[self.pos].isspace():
            self.pos += 1

    def next_token(self) -> Token:
        """
        Parses the first token in the string.
        Skips leading spaces from the current position and parse the token
        :return: Next parsed token
        :raise AssertionError: if the token cannot be parsed
        """
        self._skip_ws()
        for key, value in self.tokens.items():
            match = re.match(value, self.string[self.pos:])
            if match is not None:
                self.pos = self.pos + match.end()
                if key == Type.SUBSTITUTION:
                    res = match.group(0)[1:]
                elif key == Type.CLEAN_STRING:
                    res = match.group(0)[1:-1]
                elif key == Type.STRING:
                    res = match.group(0)
                    if res[0] == '"':
                        res = res[1:-1]
                else:
                    res = match.group(0)
                return Token(res, key)
        raise AssertionError(f'Token not found, unparsed: "{self.string[self.pos:]}"')

    def parse(self) -> List[Token]:
        """
        Parse all line
        :return: List of parsed tokens
        :raise AssertionError: if the token cannot be parsed
        """
        res = []
        val = None
        while val is None or val.type != Type.END:
            val = self.next_token()
            res.append(val)
        return res
