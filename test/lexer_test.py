from test.output_fsm import output_fsm

from common.fsm_converter import Converter
from common.eq_symbols import EqualSymbols
from lexer.nfa import LexerNFA
from lexer.re_parser import REParser
from lexer.dfa import LexerDFA
from lexer.token import TokenType

parser = REParser(LexerNFA)
converter = Converter()


def test_json_number():
    token = TokenType("json number", "-?(0|[1-9][0-9]*)(\\.[0-9][0-9]*)?([eE][-+]?[0-9][0-9]*)?")

    nfa = parser.parse(token.regex)
    output_fsm(nfa, "json_number_nfa")

    eq_symbols = EqualSymbols(nfa)
    dfa = converter.convert(nfa, eq_symbols, LexerDFA, "NFAStates")


def test_json_string():
    control_characters = ''.join([chr(i) for i in range(32)])
    control_characters += chr(127)
    token = TokenType("json string", r'"([^"\\{0}]|\\["\\/bfnrtu])*"'.format(control_characters))

    nfa = parser.parse(token.regex)
    eq_symbols = EqualSymbols(nfa)
    dfa = converter.convert(nfa, eq_symbols, LexerDFA, "NFAStates")

    output_fsm(dfa, "json_string_nfa")

def test():
    test_json_number()
    # test_json_string()

test()
