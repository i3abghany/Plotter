from expr_parser.AST import AST
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
            return self.variable_map[node.identifier_token.value]

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
