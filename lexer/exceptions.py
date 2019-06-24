class RESyntaxError(BaseException):
    def __init__(self, pos, msg):
        super(RESyntaxError, self).__init__(pos, msg)


class RecognizeError(BaseException):
    def __init__(self, recognizer, msg):
        super(RecognizeError, self).__init__(recognizer, msg)
