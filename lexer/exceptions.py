class RESyntaxError(BaseException):
    def __init__(self, pos, parsing):
        self.pos = pos
        self.parsing = parsing

class RecognizeError(BaseException):
    pass