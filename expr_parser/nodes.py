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


class ParenthesizedExpressionNode:
    def __init__(self, open_paren, main_expression, close_paren):
        self.open_paren = open_paren
        self.main_expression = main_expression
        self.close_paren = close_paren

    def get_children(self):
        return [
            self.open_paren,
            self.main_expression,
            self.close_paren
        ]
