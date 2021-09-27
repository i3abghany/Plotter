from expr_parser.lexer import Lexer
from expr_parser.tokens import Token, TokenKind
from expr_parser.AST import AST
from expr_parser.nodes import *


class Parser:
    def __init__(self, text: str):
        """ Generates an abstract syntax tree for a internally-generated token list from the input string @text.

        :param text: The string expression for which er generate the abstract syntax tree.
        """
        self.lexer = Lexer(text)
        self.tokens = self.lexer.tokenize()
        self.position = 0
        self.errors = self.lexer.errors
        self.identifiers = set()
        self.binary_operator_precedences = {
            TokenKind.PLUS: 1,
            TokenKind.MINUS: 1,
            TokenKind.STAR: 2,
            TokenKind.SLASH: 2,
            TokenKind.CARET: 4
        }

        self.unary_operator_precedences = {
            TokenKind.PLUS: 4,
            TokenKind.MINUS: 4,
        }

    def get_binary_operator_precedence(self, kind):
        try:
            return self.binary_operator_precedences[kind]
        except KeyError:
            return 0

    def get_unary_operator_precedence(self, kind):
        try:
            return self.unary_operator_precedences[kind]
        except KeyError:
            return 0

    def parse_parenthesized_expression(self):
        """ Parse an expression enclosed in parentheses in the following form:
            ( EXPRESSION )

        :rtype: ParenthesizedExpressionNode
        :return: A parenthesized expression AST node.
        """
        open_paren = self.match_if(TokenKind.LEFT_PAREN)
        main_expression = self.parse_expression()
        close_paren = self.match_if(TokenKind.RIGHT_PAREN)

        return ParenthesizedExpressionNode(open_paren, main_expression, close_paren)

    def parse_primary_expression(self):
        """ Parse an expression of highest priority. This could be either a parenthesized expression,
         an identifier, a unary expression, or a number expression.

        :return: A primary expression AST node.
        """
        if self.does_match(TokenKind.LEFT_PAREN):
            return self.parse_parenthesized_expression()

        if self.does_match(TokenKind.IDENTIFIER):
            identifier_token = self.match_if(TokenKind.IDENTIFIER)
            self.identifiers.add(identifier_token.value)
            return IdentifierNode(identifier_token)

        if self.does_match(TokenKind.PLUS):
            plus_token = self.match_if(TokenKind.PLUS)
            operand = self.parse_expression()
            return UnaryExpressionNode(plus_token, operand)
        elif self.does_match(TokenKind.MINUS):
            minus_token = self.match_if(TokenKind.MINUS)
            operand = self.parse_expression()
            return UnaryExpressionNode(minus_token, operand)

        number_token = self.match_if(TokenKind.NUMBER)
        return NumberExpressionNode(number_token)

    def parse(self):
        """ The public interface of a Parser, generates the full AST from the input string at
        construction time.

        It expects an EOF token after exactly one full expression, so an expression like 1 1 would not work.

        :rtype: AST
        :return: the AST of the input expression
        """
        expression = self.parse_expression()
        eof_token = self.match_if(TokenKind.EOF)
        return AST(self.errors, expression, eof_token, self.identifiers)

    def parse_expression(self, parent_precedence=0):
        """ Calls itself recursively based on operator precedences to parse a full expression.
        Unary expressions are of highest priority, they're consumed at the start of expression parsing,
        if any unary operators exist.

        :rtype ExpressionNode
        :return Returns a node of type NumberExpressionNode, IdentifierNode, ParenthesizedExpressionNode,
         BinaryExpressionNode or a UnaryExpressionNode
        """
        current = self.get_current()
        unary_operator_precedence = self.get_unary_operator_precedence(current.kind)
        if unary_operator_precedence != 0 and unary_operator_precedence >= parent_precedence:
            unary_operator = self.next_token()
            operand = self.parse_expression(unary_operator_precedence)
            left = UnaryExpressionNode(unary_operator, operand)
        else:
            left = self.parse_primary_expression()

        while True:
            precedence = self.get_binary_operator_precedence(self.get_current().kind)
            if precedence == 0 or precedence <= parent_precedence:
                break

            operator_token = self.next_token()
            right = self.parse_expression(precedence)
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
