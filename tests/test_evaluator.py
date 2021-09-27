import unittest

from evaluator import Evaluator
from expr_parser.parser import Parser


class TestEvaluator(unittest.TestCase):

    @staticmethod
    def get_result(expr, *kwargs):
        parser = Parser(expr)
        ast = parser.parse()
        evaluator = Evaluator(ast)
        if len(kwargs) > 1:
            evaluator.set_var(kwargs[0], kwargs[1])
        return evaluator.eval()

    def test_simple_addition(self):
        expr = '12 + 3'
        result = self.get_result(expr)
        self.assertEqual(result, 12 + 3)

    def test_precedence(self):
        expr = '3 + 2 * 4'
        result = self.get_result(expr)
        self.assertEqual(result, 3 + 2 * 4)

        expr = '2 * 3 + 4'
        result = self.get_result(expr)
        self.assertEqual(result, 2 * 3 + 4)

    def test_parenthesized_expr(self):
        expr = '(4 + 2) * 3'
        result = self.get_result(expr)
        self.assertEqual(result, (4 + 2) * 3)

    def test_exponentiation(self):
        expr = '2 ^ -10 + 1233123'
        result = self.get_result(expr)
        self.assertEqual(result, 2 ** -10 + 1233123)

    def test_substitution(self):
        expr = 'x ^ 4 * 123 + 4'
        x = 29
        result = self.get_result(expr, 'x', x)
        self.assertEqual(result, x ** 4 * 123 + 4)

    def test_multiple_substitutions(self):
        expr = '2*x^4 + 4 * x - 12'
        x = 3
        result = self.get_result(expr, 'x', x)
        self.assertEqual(result, 2 * x ** 4 + 4 * x - 12)

    def test_parenthesized_exponentiation(self):
        expr = '5 * x ^ (2 * (3 + 4))'
        x = 2
        result = self.get_result(expr, 'x', x)
        self.assertEqual(result, 5 * x ** (2 * (3 + 4)))

    def test_simple_unary_operation(self):
        expr = '-2'
        result = self.get_result(expr)
        self.assertEqual(result, -2)

    def test_compound_unary_operators(self):
        expr = '-2 * x ^ -3'
        result = self.get_result(expr, 'x', 4)
        x = 4
        self.assertEqual(result, -2 * x ** -3)

        result = self.get_result(expr, 'x', 3.141592)
        x = 3.141592
        self.assertEqual(result, -2 * x ** -3)

    def test_multiple_unary_operators(self):
        expr = '-------------+++++++++++++++++++-----++-+-------------------3'
        result = self.get_result(expr)
        self.assertEqual(result, -------------+++++++++++++++++++-----++-+-------------------3)
