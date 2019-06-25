class Token:
    def __init__(self, sentence, token_type):
        self.sentence = sentence
        self.token_type = token_type

    def __str__(self):
        return "type: {0}, sentence: {1}".format(self.token_type.name, self.sentence)

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