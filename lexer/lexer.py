from functools import reduce
from lexer.re_parser import REParser
from lexer.converter import Converter
from lexer.dfa import DFA
from lexer.nfa import NFA
from lexer.token import TokenType, Token
from lexer.recognizer import Recognizer
from lexer.symbol_translation import SymbolTranslation


class Lexer:
    def __init__(self):
        self.re_parser = REParser(NFA)
        self.converter= Converter(DFA)
        self.recognizer = Recognizer(Token)
        self.token_types = []

    def set_token(self, regex, name, annotation=""):
        self.token_types.append(TokenType(regex, name, annotation))

    def lex(self, input_string):
        nfa_accepting_mapper = {}
        nfas = []
        for token_type in self.token_types:
            nfa = self.re_parser.parse(token_type.regex)
            for state in nfa.accepting_states:
                nfa_accepting_mapper[state.index] = token_type
            nfas.append(nfa)
        complete_nfa = reduce(lambda nfa1, nfa2: nfa1.union(nfa2), nfas)

        nfa_symbol_translation = self.make_translation(complete_nfa.compact_symbol_sets)

        result = self.converter.convert(complete_nfa, nfa_accepting_mapper, nfa_symbol_translation)
        dfa = result['dfa']
        dfa_accepting_mapper = result['accepting_mapper']

        dfa_symbol_translation = self.make_translation(dfa.compact_symbol_sets)

        final_transition = nfa_symbol_translation.concat(dfa_symbol_translation)

        return self.recognizer.recognize(input_string, dfa, dfa_accepting_mapper, final_transition)

    @staticmethod
    def make_translation(compact_symbol_sets):
        nfa_symbol_translation = SymbolTranslation()
        for index, symbol_set in enumerate(compact_symbol_sets):
            for symbol in symbol_set:
                nfa_symbol_translation[symbol] = index
        return nfa_symbol_translation
