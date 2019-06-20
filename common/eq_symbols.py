from typing import Dict, Any, Tuple, Set
from random import sample
from collections import defaultdict

from common.fsm import NFA
from common.symbol import epsilon


class EqualSymbols:
    def __init__(self, nfa: NFA):
        self.nfa = nfa
        self.sigma = None
        self._symbol_translation = None
        self.calculate()

    def calculate(self):
        m = defaultdict(tuple)                                                          # type: Dict[Any, Tuple]

        for edge in self.nfa.edges:
            src = edge.src_state
            dest = edge.dest_state
            symbol = edge.symbol
            if symbol is not epsilon:
                uv = (src, dest)
                m[symbol] += (uv, )

        reversed_m = defaultdict(set)                                                   # type: Dict[Tuple, Set[Any]]
        for symbol, uvs in m.items():
            reversed_m[uvs].add(symbol)

        symbol_translation = {}                                                         # type: Dict[Any, int]
        sigma = set()
        i = 1
        for symbols in reversed_m.values():
            for symbol in symbols:
                symbol_translation[symbol] = i
            i += 1
            sigma.add(*sample(symbols, 1))

        self._symbol_translation = symbol_translation
        self.sigma = sigma

    def index(self, symbol):
        return self._symbol_translation[symbol]

