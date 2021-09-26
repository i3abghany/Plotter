from expr_parser.lexer import Lexer
from expr_parser.tokens import Token, TokenKind
from expr_parser.AST import AST
from expr_parser.nodes import *


class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.tokens = self.lexer.tokenize()
        self.position = 0
        self.errors = self.lexer.errors

    def parse_parenthesized_expression(self):
        open_paren = self.match_if(TokenKind.LEFT_PAREN)
        main_expression = self.parse_term()
        close_paren = self.match_if(TokenKind.RIGHT_PAREN)

        return ParenthesizedExpressionNode(open_paren, main_expression, close_paren)

    def parse_primary_expression(self):
        if self.does_match(TokenKind.LEFT_PAREN):
            return self.parse_parenthesized_expression()

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

    def parse_exponentiated_factor(self):
        left = self.parse_primary_expression()

        while self.get_current().kind == TokenKind.CARET:
            operator_token = self.next_token()
            right = self.parse_primary_expression()
            left = BinaryExpressionNode(left, operator_token, right)

        return left

    def parse_factor(self):
        left = self.parse_exponentiated_factor()

        while self.get_current().kind == TokenKind.STAR or \
                self.get_current().kind == TokenKind.SLASH:
            operator_token = self.next_token()
            right = self.parse_exponentiated_factor()
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
