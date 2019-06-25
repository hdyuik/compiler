from typing import Dict, Any, Tuple, Set
from random import sample
from collections import defaultdict

from .fsm import NFA
from .symbol import epsilon


class EqualSymbols:
    def __init__(self, nfa: NFA):
        self.nfa = nfa
        self.sigma = None
        self.mapper = None
        self.reversed_mapper = None
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

        reversed_translation = defaultdict(set)                                         # type: Dict[int, Set[Any]]
        symbol_translation = {}                                                         # type: Dict[Any, int]
        sigma = set()
        i = 1
        for symbols in reversed_m.values():
            reversed_translation[i].update(symbols)
            for symbol in symbols:
                symbol_translation[symbol] = i

            i += 1
            sigma.add(*sample(symbols, 1))

        self.reversed_mapper = reversed_translation
        self.mapper = symbol_translation
        self.sigma = sigma

    def index(self, symbol):
        return self.mapper[symbol]

    def symbols(self, index):
        return self.reversed_mapper[index]

