class AST:

    def __init__(self, errors, main_expression, eof_token):
        self.main_expression = main_expression
        self.eof_token = eof_token
        self.errors = errors


def print_ast(node, indent="", is_last=True):
    if node is None:
        return

    indent_extension = '└── ' if is_last else '├── '

    print(indent, end='')
    print(indent_extension, end='')

    print(type(node).__name__, end='')
    if type(node).__name__ == 'Token' and node.value is not None:
        print(' ' + str(node.value), end='')

    print()

    indent += '    ' if is_last else '│    '

    for i, e in enumerate(node.get_children()):
        print_ast(e, indent, i == len(node.get_children()) - 1)
