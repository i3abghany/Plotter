from expr_parser.tokens import Token, TokenKind


def is_part_of_number_token(c):
    return c in '0123456789.'


def is_whitespace(c):
    return c in ' \t\n\r'


def is_part_of_identifier_token(c):
    return c.isalpha() or c == '_'


class Lexer:
    def __init__(self, line):
        self.current = None
        self.position = -1
        self.tokens = []
        self.errors = []
        self.text_repr = iter(line)
        self.next_char()

    def next_char(self):
        try:
            self.current = next(self.text_repr)
            self.position += 1
        except StopIteration:
            self.current = None

    def tokenize(self):
        while self.current is not None:
            if is_whitespace(self.current):
                self.next_char()
                continue
            elif self.current.isdigit():
                self.tokens.append(self.lex_number())
                continue
            elif is_part_of_identifier_token(self.current):
                self.tokens.append(self.lex_identifier())
                continue
            elif self.current == '(':
                self.tokens.append(Token(TokenKind.LEFT_PAREN, None, self.position))
            elif self.current == ')':
                self.tokens.append(Token(TokenKind.RIGHT_PAREN, None, self.position))
            elif self.current == '*':
                self.tokens.append(Token(TokenKind.STAR, None, self.position))
            elif self.current == '/':
                self.tokens.append(Token(TokenKind.SLASH, None, self.position))
            elif self.current == '+':
                self.tokens.append(Token(TokenKind.PLUS, None, self.position))
            elif self.current == '-':
                self.tokens.append(Token(TokenKind.MINUS, None, self.position))
            else:
                self.errors.append(f'Lexer Error: Unexpected character \'{self.current}\' at column {self.position}')
                self.tokens.append(Token(TokenKind.BAD, self.current, self.position))

            self.next_char()

        self.tokens.append(Token(TokenKind.EOF, None, self.position + 1))
        return self.tokens

    def lex_number(self):
        str_number = ''
        position = self.position
        one_decimal_point: bool = False
        while (self.current is not None) and is_part_of_number_token(self.current):

            if self.current == '.' and one_decimal_point:
                break

            if self.current == '.':
                one_decimal_point = True

            str_number += self.current
            self.next_char()

        return Token(TokenKind.NUMBER, float(str_number), position)

    def lex_identifier(self):
        name = ''
        position = self.position
        while self.current is not None and is_part_of_identifier_token(self.current):
            name += self.current
            self.next_char()

        return Token(TokenKind.IDENTIFIER, name, position)
