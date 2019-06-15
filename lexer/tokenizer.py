from functools import reduce
from lexer.re_parser import REParser
from lexer.converter import Converter
from lexer.dfa import DFA
from lexer.nfa import NFA
from lexer.token import TokenType, Token
from lexer.recognizer import Recognizer


class Lexer:
    def __init__(self):
        self.re_parser = REParser(NFA)
        self.converter= Converter(DFA)
        self.recognizer = Recognizer(Token)
        self.token_types = []

    def set_token(self, regex, name, annotation=""):
        self.token_types.append(TokenType(regex, name, annotation))

    def lex(self, input_string):
        accepting_mapper = {}
        nfas = []
        for token_type in self.token_types:
            nfa = self.re_parser.parse(token_type.regex)
            for state in nfa.accepting_states:
                accepting_mapper[state.index] = token_type
            nfas.append(nfa)

        complete_nfa = reduce(lambda nfa1, nfa2: nfa1.union(nfa2), nfas)

        result = self.converter.convert(complete_nfa, accepting_mapper)

        dfa = result['dfa']
        dfa_accepting_mapper = result['accepting_mapper']

        self.recognizer.recognize(input_string, dfa, dfa_accepting_mapper)

