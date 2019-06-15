from lexer.nfa import NFA
from lexer.re_parser import REParser


parser = REParser(NFA)


def test_json_number():
    nfa = parser.parse("-?(0|[1-9][0-9]*)(\\.[0-9][0-9]*)?([eE][-+]?[0-9][0-9]*)?")
    nfa.display()

def test():
    test_json_number()
    pass

test()
