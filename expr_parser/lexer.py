from expr_parser.tokens import Token, TokenKind


class Lexer:
    def __init__(self, line: str):
        """ Tokenizes a string into well-defined tokens.

        :param line: String to generate a list of tokens from.
        """
        self.current = None
        self.position = -1
        self.tokens = []
        self.errors = []
        self.text_repr = iter(line)
        self.__next_char()

    def tokenize(self):
        """ Generates a list of token for the string provided at construction-time.

        :rtype: list[Token]
        :return: a list of tokens, the types of those tokens are defined in expr_parser.tokens
        """
        while self.current is not None:
            if is_whitespace(self.current):
                self.__next_char()
                continue
            elif self.current.isdigit():
                self.tokens.append(self.__lex_number())
                continue
            elif is_part_of_identifier_token(self.current):
                self.tokens.append(self.__lex_identifier())
                continue
            elif self.current == '(':
                self.tokens.append(Token(TokenKind.LEFT_PAREN, self.current, self.position))
            elif self.current == ')':
                self.tokens.append(Token(TokenKind.RIGHT_PAREN, self.current, self.position))
            elif self.current == '*':
                self.tokens.append(Token(TokenKind.STAR, self.current, self.position))
            elif self.current == '/':
                self.tokens.append(Token(TokenKind.SLASH, self.current, self.position))
            elif self.current == '+':
                self.tokens.append(Token(TokenKind.PLUS, self.current, self.position))
            elif self.current == '-':
                self.tokens.append(Token(TokenKind.MINUS, self.current, self.position))
            elif self.current == '^':
                self.tokens.append(Token(TokenKind.CARET, self.current, self.position))
            else:
                self.errors.append(f'Lexer Error: Unexpected character \'{self.current}\' at column {self.position}')
                self.tokens.append(Token(TokenKind.BAD, self.current, self.position))

            self.__next_char()

        self.tokens.append(Token(TokenKind.EOF, None, self.position + 1))
        return self.tokens

    def __next_char(self):
        try:
            self.current = next(self.text_repr)
            self.position += 1
        except StopIteration:
            self.current = None

    def __lex_number(self):
        str_number = ''
        position = self.position
        one_decimal_point: bool = False
        while (self.current is not None) and is_part_of_number_token(self.current):

            if self.current == '.' and one_decimal_point:
                break

            if self.current == '.':
                one_decimal_point = True

            str_number += self.current
            self.__next_char()

        return Token(TokenKind.NUMBER, float(str_number), position)

    def __lex_identifier(self):
        name = ''
        position = self.position
        while self.current is not None and is_part_of_identifier_token(self.current):
            name += self.current
            self.__next_char()

        return Token(TokenKind.IDENTIFIER, name, position)


def is_part_of_number_token(c):
    return c in '0123456789.'


def is_whitespace(c):
    return c in ' \t\n\r'


def is_part_of_identifier_token(c):
    return c.isalpha() or c == '_'
