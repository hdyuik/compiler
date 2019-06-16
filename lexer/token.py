class Token:
    def __init__(self, symbols, token_type):
        self.symbols = symbols
        self.token_type = token_type


class TokenType:
    count = 0
    def __init__(self, name, regex, annotation=""):
        TokenType.count += 1
        self.index = TokenType.count
        self.name = name
        self.regex = regex
        self.annotation = annotation

    def __repr__(self):
        return "Token: {0}".format(self.name)