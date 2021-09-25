import unittest

from expr_parser.parser import *


class TestParser(unittest.TestCase):

    def test_empty_expr(self):
        parser = Parser('')
        ast = parser.parse()
        errors = ast.errors
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith('Parser Error'))

    def test_parse_simple_add(self):
        parser = Parser('1 + 2')
        ast = parser.parse()
        root_node = ast.main_expression

        self.assertTrue(isinstance(root_node, BinaryExpressionNode))
        self.assertTrue(isinstance(root_node.left_expression, NumberExpressionNode))
        self.assertEqual(root_node.operator_token.kind, TokenKind.PLUS)
        self.assertTrue(isinstance(root_node.right_expression, NumberExpressionNode))

    def test_parse_compound_add(self):
        parser = Parser('1 + 2 + 3')
        ast = parser.parse()
        root_node = ast.main_expression
        self.assertTrue(isinstance(root_node, BinaryExpressionNode))
        self.assertTrue(isinstance(root_node.left_expression, BinaryExpressionNode))

        left_expr = root_node.left_expression
        self.assertTrue(isinstance(left_expr.left_expression, NumberExpressionNode))
        self.assertEqual(left_expr.operator_token.kind, TokenKind.PLUS)
        self.assertTrue(isinstance(left_expr.right_expression, NumberExpressionNode))

        self.assertEqual(root_node.operator_token.kind, TokenKind.PLUS)
        self.assertTrue(isinstance(root_node.right_expression, NumberExpressionNode))

    def test_expect_number(self):
        expr = '1 + '
        parser = Parser(expr)
        ast = parser.parse()
        errors = ast.errors
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0], 'Parser Error: Unexpected token of type \'EOF\', expected \'NUMBER\'.')

    def test_expect_eof_after_full_expression(self):
        expr = '1 1'
        parser = Parser(expr)
        ast = parser.parse()
        errors = ast.errors
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0], 'Parser Error: Unexpected token 1.0 of type \'NUMBER\', expected \'EOF\'.')
