from expr_parser.lexer import Lexer
from expr_parser.tokens import Token, TokenKind


class NumberExpressionNode:
    def __init__(self, number_token):
        self.number_token = number_token

    def get_children(self):
        return [self.number_token]


class IdentifierNode:
    def __init__(self, identifier_token):
        self.identifier_token = identifier_token

    def get_children(self):
        return [self.identifier_token]


class BinaryExpressionNode:
    def __init__(self, left_expression, operator_token, right_expression):
        self.left_expression = left_expression
        self.operator_token = operator_token
        self.right_expression = right_expression

    def get_children(self):
        return [
            self.left_expression,
            self.operator_token,
            self.right_expression
        ]


def print_ast(node, indent="", is_last=True):
    if node is None:
        return

    indent_extension = '└── ' if is_last else '├── '

    print(indent, end='')
    print(indent_extension, end='')

    print(type(node).__name__, end='')
    if type(node).__name__ == 'Token' and node.value is not None:
        print(' ' + str(node.value), end='')

    print()

    indent += '    ' if is_last else '│    '

    for i, e in enumerate(node.get_children()):
        print_ast(e, indent, i == len(node.get_children()) - 1)


class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.tokens = self.lexer.tokenize()
        self.position = 0
        self.errors = self.lexer.errors

    def parse_primary_expression(self):
        if self.does_match(TokenKind.IDENTIFIER):
            identifier_token = self.match_if(TokenKind.IDENTIFIER)
            return IdentifierNode(identifier_token)

        number_token = self.match_if(TokenKind.NUMBER)
        return NumberExpressionNode(number_token)

    def parse(self):
        expression = self.parse_term()
        eof_token = self.match_if(TokenKind.EOF)
        return AST(self.errors, expression, eof_token)

    def parse_term(self):
        left = self.parse_factor()
        while self.get_current().kind == TokenKind.PLUS or \
                self.get_current().kind == TokenKind.MINUS:
            operator_token = self.next_token()
            right = self.parse_factor()
            left = BinaryExpressionNode(left, operator_token, right)

        return left

    def parse_factor(self):
        left = self.parse_primary_expression()

        while self.get_current().kind == TokenKind.STAR or \
                self.get_current().kind == TokenKind.SLASH:
            operator_token = self.next_token()
            right = self.parse_primary_expression()
            left = BinaryExpressionNode(left, operator_token, right)

        return left

    def does_match(self, token_kind):
        return self.get_current().kind == token_kind

    def match_if(self, token_kind):
        if self.get_current().kind == token_kind:
            return self.next_token()
        else:
            value = self.get_current().value
            kind_name = self.get_current().kind.name
            self.errors.append(
                f'Parser Error: Unexpected token{" " + str(value) if value is not None else ""} '
                f'of type \'{kind_name}\', expected \'{token_kind.name}\'.')
            return Token(token_kind, None, self.get_current().position)

    def next_token(self):
        ret = self.get_current()
        self.position += 1
        return ret

    def peek(self, offset):
        index = self.position + offset
        if index >= len(self.tokens):
            return self.tokens[len(self.tokens) - 1]
        else:
            return self.tokens[index]

    def get_current(self):
        return self.peek(0)


class AST:

    def __init__(self, errors, main_expression, eof_token):
        self.main_expression = main_expression
        self.eof_token = eof_token
        self.errors = errors
