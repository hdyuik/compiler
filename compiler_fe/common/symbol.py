class Symbol:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return "{0}".format(self.name)


class NonTerminal(Symbol):
    pass


class Terminal(Symbol):
    pass


epsilon = Terminal("ε")
EOF = Terminal("EOF")