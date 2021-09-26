import numpy as np

from expr_parser.nodes import *
from expr_parser.tokens import *


class Evaluator:
    def __init__(self, ast):
        self.ast = ast
        self.variable_map = {}

    def set_var(self, name, val):
        self.variable_map[name] = val

    def eval(self):
        return self.__eval(self.ast.main_expression)

    def __eval(self, node):
        if isinstance(node, NumberExpressionNode):
            return node.number_token.value
        if isinstance(node, IdentifierNode):
            try:
                return self.variable_map[node.identifier_token.value]
            except KeyError:
                raise Exception(f"Evaluation Error: invalid identifier {node.identifier_token.value}")

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



def evaluate_in_range(ast, min_x=0, max_x=1, delta=0.0):
    if min_x > max_x:
        min_x, max_x = max_x, min_x

    if delta == 0.0:
        delta = (max_x - min_x) / 50000

    x_range = np.arange(min_x, max_x, delta)
    y_values = []

    evaluator = Evaluator(ast)

    for x_point in np.arange(min_x, max_x, delta):
        evaluator.set_var('x', x_point)
        y_values.append(evaluator.eval())

    return x_range, y_values
