class GrammarError(BaseException):
    def __init__(self, msg):
        self.msg = msg


class AnalyzeError(BaseException):
    def __init__(self, analyzer, msg):
        super(AnalyzeError, self).__init__('can not parse, detail in Error.parsing_stack, Error.input_stack')
        self.parsing_stack = '    '.join([str(item)for item in analyzer._parsing_stack])
        self.input_stack = '  '.join([str(item) for item in analyzer._inputs])
        self.msg = msg
