class AST:
    def __init__(self, root_symbol, rule, *children):
        self.root_symbol = root_symbol
        self.rule = rule
        self.children = children

    def __str__(self):
        return str(self.root_symbol)


class Leaf(AST):
    def __init__(self, root_symbol, actual_input):
        super(Leaf, self).__init__(root_symbol, None)
        self.actual_input = actual_input

    def __str__(self):
        return str(self.actual_input)

