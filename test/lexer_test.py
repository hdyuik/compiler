from lexer.nfa import NFA
from lexer.re_parser import REParser
from lexer.converter import Converter
from lexer.dfa import DFA

parser = REParser(NFA)
converter = Converter(DFA)


def test_json_number():
    nfa = parser.parse("-?(0|[1-9][0-9]*)(\\.[0-9][0-9]*)?([eE][-+]?[0-9][0-9]*)?")
    converter.convert(nfa, )
    print("cb: ", nfa.cb)
    print("ucb: ", nfa.icb)

def test():
    test_json_number()
    pass

test()
