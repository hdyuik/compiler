class Token:
    def __init__(self, symbols, token_type):
        self.symbols = symbols
        self.token_type = token_type


class TokenType:
    count = 0
    def __init__(self, regex, name, annotation=""):
        TokenType.count += 1
        self.index = TokenType.count
        self.regex = regex
        self.name = name
        self.annotation = annotation