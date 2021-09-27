import multiprocessing
import functools

import numpy as np

from expr_parser.nodes import *

from expr_parser.tokens import *


class Evaluator:
    def __init__(self, ast):
        """ Evaluates an expression represented by an AST object.
        :type ast: AST
        :param ast: An abstract syntax tree representing an expression.

        """
        self.ast = ast
        self.variable_map = {}

    def set_var(self, name, val):
        """ Sets the value of an identifier to use for evaluation.
        
        Since the AST may contain multiple identifiers, the user of the evaluator must set the values
        for those identifiers before calling `evaluate`.
        
        :type name: str
        :param name: The name of the identifier
        
        :param val: The value to substitute in the place of an identifier
        :type val: float
        """
        if name in self.ast.identifiers:
            self.variable_map[name] = val
        else:
            raise KeyError(f"Evaluation Error: Invalid Identifier \'{name}\'")

    def eval(self):
        """ An interface method to evaluate the AST provided at construction-time.
        
        :rtype float
        :return: The result of the evaluation.
        """
        return self.__eval(self.ast.main_expression)

    def __eval(self, node):
        """ Internal recursive utility that evaluates the value of a tree starting from the node `node`.
        
        :param node: The root of the subtree to evaluate.
        :return: A float value of the operations represented by the subtree.
        """
        if isinstance(node, NumberExpressionNode):
            return node.number_token.value
        if isinstance(node, IdentifierNode):
            try:
                return self.variable_map[node.identifier_token.value]
            except KeyError:
                raise Exception(f"Evaluation Error: Invalid identifier {node.identifier_token.value}")

        if isinstance(node, ParenthesizedExpressionNode):
            return self.__eval(node.main_expression)
        elif isinstance(node, BinaryExpressionNode):
            left = self.__eval(node.left_expression)
            right = self.__eval(node.right_expression)

            if node.operator_token.kind == TokenKind.PLUS:
                return left + right
            elif node.operator_token.kind == TokenKind.MINUS:
                return left - right
            elif node.operator_token.kind == TokenKind.STAR:
                return left * right
            elif node.operator_token.kind == TokenKind.SLASH:
                return left / right
            elif node.operator_token.kind == TokenKind.CARET:
                return left ** right
            else:
                raise Exception(f"Evaluation Error: Invalid binary operator \'{node.operator_token.kind.name}\'")
        elif isinstance(node, UnaryExpressionNode):
            if node.operator_token.kind == TokenKind.PLUS:
                return self.__eval(node.operand)
            elif node.operator_token.kind == TokenKind.MINUS:
                return -self.__eval(node.operand)
            else:
                raise Exception(f"Evaluation Error: Invalid unary operator \'{node.operator_token.kind.name}\'")


def get_y(evaluator, x_point):
    evaluator.set_var('x', x_point)
    return evaluator.eval()


def evaluate_in_range(ast, min_x=0, max_x=1, delta=0.0, n_points=50000):
    """ Evaluates an AST object in the defined range.

    :param ast: The AST object to evaluate.
    :param min_x: Lower bound of the evaluation interval.
    :param max_x: Upper bound of the evaluation interval.
    :param delta: Space between two adjacent point on the x-axis
    :type delta: float
    :return Evenly-spaced x-values within the interval [min_x, max_x), and the corresponding y values.
    """
    if min_x > max_x:
        min_x, max_x = max_x, min_x

    if min_x == max_x:
        return [], []

    if delta == 0.0:
        delta = (max_x - min_x) / n_points

    x_range = np.arange(min_x, max_x, delta)

    evaluator = Evaluator(ast)
    thread_pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    y_values = thread_pool.map(functools.partial(get_y, evaluator), x_range)

    thread_pool.close()
    thread_pool.join()

    return x_range, y_values
