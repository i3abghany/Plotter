import enum


class TokenKind(enum.Enum):
    BAD = -1
    NUMBER = 0
    PLUS = 1
    MINUS = 2
    STAR = 3
    SLASH = 4
    CARET = 5
    IDENTIFIER = 6
    LEFT_PAREN = 7
    RIGHT_PAREN = 8
    EOF = 9


class Token:
    kind: TokenKind
    value: any = None

    def __init__(self, token_kind, value, position):
        self.kind = token_kind
        self.value = value
        self.position = position

    def __repr__(self):
        return f'Token({self.kind.name}, {str(self.value) + ", " if self.value is not None else ""}{self.position})'

    def __eq__(self, other):
        return self.kind == other.kind and self.value == other.value and self.position == other.position

    def get_children(self):
        return []
