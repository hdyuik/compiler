from functools import reduce

from common.fsm_converter import Converter
from common.eq_symbols import EqualSymbols
from lexer.re_parser import REParser
from lexer.dfa import LexerDFA
from lexer.nfa import LexerNFA
from lexer.token import TokenType


class Lexer:
    def __init__(self):
        self.re_parser = REParser(LexerNFA)
        self.converter= Converter()
        self.token_types = []

    def set_token(self, name, regex, annotation=""):
        self.token_types.append(TokenType(name, regex, annotation))

    def lex(self, input_string):
        nfas = []
        for token_type in self.token_types:
            nfa = self.re_parser.parse(token_type.regex)
            for state in nfa.accepting_states:
                state.items['token'] = token_type
            nfas.append(nfa)
        complete_nfa = reduce(lambda nfa1, nfa2: nfa1.union(nfa2), nfas)
        nfa_eq_symbols = EqualSymbols(complete_nfa)

        dfa = self.converter.convert(
            nfa=complete_nfa,
            eq_symbols=nfa_eq_symbols,
            dfa_class=LexerDFA,
            item_attr_name="NFAStates",
        )
        dfa_eq_symbols = EqualSymbols(dfa)
