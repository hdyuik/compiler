from functools import reduce

from common import Converter, EqualSymbols, EOF
from lexer.re_parser import REParser
from lexer.dfa import LexerDFA
from lexer.nfa import LexerNFA
from lexer.recognizer import Recognizer


class Lexer:
    re_parser = REParser(LexerNFA)
    def __init__(self, token_types, skip_chars):
        self.token_types = token_types

        self.nfa = None
        self.dfa = None
        self.eq_symbols = None
        self.key_func = None
        self.recognizer = None
        self.skip_chars = skip_chars

        self.prepare()

    def prepare(self):
        nfas = []
        for token_type in self.token_types:
            nfa = self.re_parser.parse(token_type.regex)
            for state in nfa.accepting_states:
                state.items.token = token_type
            nfas.append(nfa)
        self.nfa = reduce(lambda nfa1, nfa2: nfa1.union(nfa2), nfas)
        self.eq_symbols = EqualSymbols(self.nfa)
        self.dfa = Converter().convert(
            nfa=self.nfa,
            eq_symbols=self.eq_symbols,
            dfa_class=LexerDFA,
        )
        self.key_func = lambda char: self.eq_symbols.index(char) if char is not EOF else EOF
        self.recognizer = Recognizer(self.dfa, self.key_func)


    def lex(self, sentence: str, skip_chars=None):
        if not skip_chars:
            skip_chars = self.skip_chars
        sentence = list(sentence) + [EOF, ]
        tokens = []
        i = 0

        while True:
            if sentence[i] == EOF:
                return tokens
            elif sentence[i] in skip_chars:
                i += 1
            else:
                token = self.recognizer.recognize(sentence, i)
                tokens.append(token)
                i += len(token.sentence)
