import enum


class TokenKind(enum.Enum):
    BAD = -1
    NUMBER = 0
    PLUS = 1
    MINUS = 2
    STAR = 3
    SLASH = 4
    IDENTIFIER = 5
    LEFT_PAREN = 6
    RIGHT_PAREN = 7


class Token:
    kind: TokenKind
    value: any = None

    def __init__(self, token_kind, value, position):
        self.kind = token_kind
        self.value = value
        self.position = position

    def __repr__(self):
        return '{kind: ' + self.kind.name + ', value: ' + str(self.value) + '}'
