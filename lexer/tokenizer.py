from lexer.re_parser import BaseParser
from lexer.converter import Converter
from lexer.dfa import DFAState, DFA


class Token:
    def __init__(self, symbols, token_info):
        self.symbols = symbols
        self.token_info = token_info


class TokenType:
    def __init__(self, regex, name, annotation=""):
        self.regex = regex
        self.name = name
        self.annotation = annotation


class Tokenizer:
    def __init__(self, re_parser: BaseParser):
        self.re_parser = re_parser
        self.nfa_2_dfa_converter = Converter(DFAState, re_parser.sigma)
        self.token_types = []

    def set_token(self, regex, name, annotation=""):
        self.token_types.append(TokenType(regex, name, annotation))

    def recognize(self, input_string):
        nfas_token_ids = []
        for index, token_type in enumerate(self.token_types):
            nfa = self.re_parser.parse(token_type.regex)
            nfas_token_ids.append((nfa, index))

        dfa_start_state = self.nfa_2_dfa_converter.convert(nfas_token_ids)
        dfa = DFA(dfa_start_state)

        tokens = [Token(chunk, self.token_types[token_id]) for chunk, token_id in dfa.recognize(input_string)]
        return tokens
