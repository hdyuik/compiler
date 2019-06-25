from typing import Dict, Set
from collections import defaultdict

from compiler_fe.common import epsilon
from .grammar import Grammar
from .lalr_nfa import LALRNFA, LALRNFAState
from .items import LookAheadItem


class FirstSet:
    def __init__(self, g: Grammar):
        self.g = g
        self._fs_table = defaultdict(set)
        self.calculate()

    def calculate(self):
        changed = True
        while changed:
            changed = False
            for rule in self.g.rules:
                previous_count = len(self._fs_table[rule.left_hand])
                for symbol in rule.right_hand:
                    if symbol in self.g.terminals:
                        self._fs_table[rule.left_hand].add(symbol)
                        break
                    else:
                        self._fs_table[rule.left_hand].update(self._fs_table[symbol])
                        if epsilon not in self._fs_table[symbol]:
                            break
                if len(self._fs_table[rule.left_hand]) != previous_count:
                    changed = True

    def __getitem__(self, symbol):
        if symbol in self.g.non_terminals:
            return self._fs_table[symbol]
        elif symbol in self.g.terminals:
            return {symbol, }
        else:
            raise Exception()


class Channelling:
    def __init__(self):
        self.first_set = None
        self.nfa = None
        self.grammar = None
        self.channel = None                                                   # type: Dict[LALRNFAState, Set[LALRNFAState]]

    def pre_configure(self, nfa: LALRNFA, g: Grammar):
        self.nfa = nfa
        self.grammar = g
        self.first_set = FirstSet(g)
        self.channel = defaultdict(set)
        for state in nfa.states:
            state.items.look_ahead = LookAheadItem(set())

    def init_channel(self):
        active_states = set()
        for edge in self.nfa.edges:
            src = edge.src_state
            dest = edge.dest_state
            symbol = edge.symbol
            if symbol is not epsilon:
                self.channel[src].add(dest)
            else:
                look_ahead_set = set()

                rule_item = src.items.rule
                unrecognized_symbols = rule_item.rule.right_hand[rule_item.dot_pos+1: ]
                for unrecognized_symbol in unrecognized_symbols:
                    first_set = self.first_set[unrecognized_symbol]
                    look_ahead_set.update(first_set)
                    if epsilon not in first_set:
                        break
                else:
                    self.channel[src].add(dest)
                if epsilon in look_ahead_set:
                    look_ahead_set.remove(epsilon)

                dest.items.look_ahead.symbols.update(look_ahead_set)
                active_states.add(dest)
        return active_states

    def flow(self, up_stream_state: LALRNFAState):
        upstream_symbols = up_stream_state.items.look_ahead.symbols

        for downstream_state in self.channel[up_stream_state]:
            downstream_symbols = downstream_state.items.look_ahead.symbols
            if not upstream_symbols.issubset(downstream_symbols):
                downstream_symbols.update(upstream_symbols)
                self.flow(downstream_state)

    def reset(self):
        self.first_set = None
        self.nfa = None
        self.grammar = None
        self.channel = None

    def channelling(self, nfa: LALRNFA, g: Grammar):
        self.pre_configure(nfa, g)
        active_states = self.init_channel()
        for state in active_states:
            self.flow(state)

        self.reset()
