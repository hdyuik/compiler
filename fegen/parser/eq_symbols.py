from fegen.common import EqualSymbols, epsilon
from .lalr_nfa import LALRNFA


class LALRNFAEqualSymbols(EqualSymbols):
    def __init__(self, nfa: LALRNFA):
        super(LALRNFAEqualSymbols, self).__init__(nfa)

    def calculate(self):
        sigma = set()
        for edge in self.nfa.edges:
            sigma.add(edge.symbol)
        sigma.remove(epsilon)
        self.sigma = sigma
        self.mapper = {symbol: symbol for symbol in sigma}
        self.reversed_mapper = {symbol: {symbol, } for symbol in sigma}

    def index(self, symbol):
        return symbol

    def symbols(self, index):
        return {index, }