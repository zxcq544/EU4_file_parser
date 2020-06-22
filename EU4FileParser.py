from typing import NamedTuple

import regex as re


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


def tokenize(string_to_tokenize):
    token_specification = [
        ('NUMBER', r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN', r'='),  # Assignment operator
        ('NEWLINE', r'[\n\r]'),  # Line endings
        ('STRING', r'[\p{L}_/.0-9-]+'),  # Unicode Strings
        ('SKIP', r'[ \t"]*'),  # Skip over spaces and tabs
        ('LBRACKET', r'{'),  # Opening bracket
        ('RBRACKET', r'}'),  # Closing bracket
        ('MISMATCH', r'.'),  # Any other character
    ]
    tok_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in token_specification))
    line_num = 1
    line_start = 0
    for i in re.finditer(tok_regex, string_to_tokenize):
        token_type = i.lastgroup
        token_value = i.group()
        column = i.start() - line_start
        if token_type == 'NUMBER':
            token_value = float(token_value) if '.' in token_value else int(token_value)
        elif token_type == 'SKIP':
            continue
        elif token_type == 'NEWLINE':
            line_start = i.end()
            line_num += 1
            continue
        elif token_type == 'MISMATCH':
            raise RuntimeError(f'{token_value!r} unexpected on line {line_num}')
        yield Token(token_type, token_value, line_num, column)


class EU4Parser:

    def __init__(self):
        self._current_token = Token("", "", 0, 0)
        self._tokens = None

    def _clean_file_before_tokenize(self, text):
        # print(text)
        text = re.sub('//', '/', text)
        # make floats normal string
        # text = re.sub(r"{ (\d.\d) (\d.\d) (\d.\d) }", r"\g<1>_\g<2>_\g<3>", text)
        # make x and y normal string
        # text = re.sub(r"{ x = (\d+) y = (\d+) }", r"x_\g<1>;y_\g<2>", text)
        # remove comments
        text = re.sub(r'#.*\n?', '', text)
        return text

    def _generate_tokens(self, text):
        self._tokens = tokenize(text)
        self._advance()

    def _advance(self):
        self._current_token = next(self._tokens, None)

    def _accept(self, token_type):
        if self._current_token and self._current_token.type == token_type:
            # self._advance()
            return True
        else:
            raise SyntaxError('Expected ' + token_type + " Current token is " + self._current_token.value)

    def _parse_pair(self):
        key_of_pair = None
        value_of_pair = None
        if self._accept("STRING"):
            key_of_pair = self._current_token.value
            self._advance()
            if self._accept("ASSIGN"):
                self._advance()
                value_of_pair = self._parse_value()
        return key_of_pair, value_of_pair

    def _parse_value(self):
        if self._current_token.type == "STRING" or self._current_token.type == "NUMBER":
            to_return = self._current_token.value
            self._advance()
            return to_return
        elif self._current_token.type == "LBRACKET":
            self._advance()
            parsed_object = None
            if self._current_token.type == "STRING":
                parsed_object = self._parse_object()
            elif self._current_token.type == "NUMBER":
                parsed_object = self._parse_color()
            return parsed_object

    def _parse_object(self):
        dic_to_return = {}
        while True:
            key, value = self._parse_pair()
            if not isinstance(value, dict):
                dic_to_return[key] = value
            else:
                if key not in dic_to_return:
                    dic_to_return[key] = value
                else:
                    if not isinstance(dic_to_return[key], list):
                        dic_to_return[key] = [dic_to_return[key], value]
                    else:
                        dic_to_return[key].append(value)
            if self._current_token.type == "RBRACKET":
                self._advance()
                return dic_to_return

    def _parse_color(self):
        color_to_return = []
        if self._current_token.type == "NUMBER":
            color_to_return.append(self._current_token.value)
            self._advance()
        if self._current_token.type == "NUMBER":
            color_to_return.append(self._current_token.value)
            self._advance()
        if self._current_token.type == "NUMBER":
            color_to_return.append(self._current_token.value)
            self._advance()
        if self._current_token.type == "RBRACKET":
            self._advance()
            return color_to_return

    def _eu4format(self):
        dic_to_return = {}
        while self._current_token:
            k, v = self._parse_pair()
            dic_to_return[k] = v
        return dic_to_return

    def parse(self, text):
        text = self._clean_file_before_tokenize(text)
        self._generate_tokens(text)
        return self._eu4format()
