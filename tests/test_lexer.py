import unittest
from expr_parser.lexer import Lexer
from expr_parser.tokens import Token, TokenKind


class TestLexer(unittest.TestCase):

    def test_empty_str(self):
        lexer = Lexer('')
        tokens = lexer.tokenize()
        self.assertEqual(len(lexer.errors), 0)
        self.assertEqual(tokens, [Token(TokenKind.EOF, None, 0)])

    def test_simple_addition(self):
        expr = '1123 + 2123'
        lexer = Lexer(expr)
        tokens = lexer.tokenize()
        self.assertEqual(len(lexer.errors), 0)

        self.assertEqual(len(tokens), 4)
        self.assertEqual(tokens[0].kind, TokenKind.NUMBER)
        self.assertEqual(tokens[0].value, 1123.0)
        self.assertEqual(tokens[0].position, expr.index('1123'))

        self.assertEqual(tokens[1].kind, TokenKind.PLUS)
        self.assertEqual(tokens[1].value, None)
        self.assertEqual(tokens[1].position, expr.index('+'))

        self.assertEqual(tokens[2].kind, TokenKind.NUMBER)
        self.assertEqual(tokens[2].value, 2123.0)
        self.assertEqual(tokens[2].position, expr.index('2123'))

        self.assertEqual(tokens[3].kind, TokenKind.EOF)
        self.assertEqual(tokens[3].position, len(expr))

    def test_compound_expression(self):
        expr = '1 + (2 * 3) / 4'
        lexer = Lexer(expr)
        tokens = lexer.tokenize()
        self.assertEqual(len(lexer.errors), 0)

        expected_tokens = [
            Token(TokenKind.NUMBER, 1.0, expr.index('1')),
            Token(TokenKind.PLUS, None, expr.index('+')),
            Token(TokenKind.LEFT_PAREN, None, expr.index('(')),
            Token(TokenKind.NUMBER, 2.0, expr.index('2')),
            Token(TokenKind.STAR, None, expr.index('*')),
            Token(TokenKind.NUMBER, 3.0, expr.index('3')),
            Token(TokenKind.RIGHT_PAREN, None, expr.index(')')),
            Token(TokenKind.SLASH, None, expr.index('/')),
            Token(TokenKind.NUMBER, 4.0, expr.index('4')),
            Token(TokenKind.EOF, None, len(expr))
        ]

        self.assertEqual(len(expected_tokens), len(tokens))

        for i, token in enumerate(tokens):
            self.assertEqual(token.value, expected_tokens[i].value)
            self.assertEqual(token.kind, expected_tokens[i].kind)

    def test_two_decimal_points(self):
        expr = '1 + 2.123.123'
        lexer = Lexer(expr)
        tokens = lexer.tokenize()
        self.assertEqual(len(lexer.errors), 1)

        expected_tokens = [
            Token(TokenKind.NUMBER, 1.0, expr.index('1')),
            Token(TokenKind.PLUS, None, expr.index('+')),
            Token(TokenKind.NUMBER, 2.123, expr.index('2.123')),
            Token(TokenKind.BAD, '.', expr.index('.')),
            Token(TokenKind.NUMBER, 123.0, expr.index('123')),
            Token(TokenKind.EOF, None, len(expr))
        ]

        for i, token in enumerate(tokens):
            self.assertEqual(token.value, expected_tokens[i].value)
            self.assertEqual(token.kind, expected_tokens[i].kind)

    def test_special_chars(self):
        expr = '!@#$'
        lexer = Lexer(expr)
        _ = lexer.tokenize()
        self.assertEqual(len(lexer.errors), 4)

