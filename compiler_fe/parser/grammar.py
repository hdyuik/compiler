from typing import List, Set, Iterator, Iterable, Dict, Tuple
import collections

from compiler_fe.common import Terminal, NonTerminal, Symbol, EOF, epsilon
from .exceptions import GrammarError
from .lalr_nfa import LALRNFA, LALRNFAState
from .items import RuleItem


RightHand = Tuple["Symbol"]


class ProductionRule:
    def __init__(self, left_hand: "NonTerminal", right_hand: RightHand):
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.check()

    def check(self):
        if not isinstance(self.left_hand, NonTerminal):
            raise GrammarError("left hand side of production rule must be NonTerminal")
        if len(self.right_hand) == 0:
            raise GrammarError("right hand side of production rule is empty(if epsilon, use epsilon terminal symbol)")
        if epsilon in self.right_hand and len(self.right_hand) > 1:
            raise GrammarError("epsilon can only show up in right hand side alone")

    def __str__(self):
        right_hand = [str(symbol) for symbol in self.right_hand]
        return "{0} -> {1}".format(self.left_hand, ' '.join(right_hand))

class RuleCollection(collections.MutableMapping):
    def __init__(self):
        self.rules = []                                                            # type: List[ProductionRule]
        self._derivations = collections.defaultdict(set)                           # type: Dict[NonTerminal, Set[RightHand]]

    def __len__(self):
        return len(self.rules)

    def __getitem__(self, non_terminal: NonTerminal) -> Set[RightHand]:
        return self._derivations[non_terminal]

    def __setitem__(self, left_hand: NonTerminal, right_hand: Iterable[Symbol]):
        right_hand = tuple(right_hand)
        self.rules.append(ProductionRule(left_hand, right_hand))
        self._derivations[left_hand].add(right_hand)

    def __delitem__(self, key):
        assert False, "not reach here"

    def __iter__(self) -> Iterator[ProductionRule]:
        return iter(self.rules)

    def __repr__(self):
        return '\n'.join(str(rule) for rule in self.rules)


class Grammar:
    def __init__(self, name: str):
        self.name = name
        self.start_symbol = None                                         # type: NonTerminal
        self.rules = RuleCollection()
        self.non_terminals = set()                                     # type: Set[NonTerminal]
        self.terminals = set()                                         # type: Set[Terminal]

    def add_rule(self, left_hand_symbol: NonTerminal, right_hand_symbols: Iterable[Symbol]):
        self.rules[left_hand_symbol] = right_hand_symbols
        self.non_terminals.add(left_hand_symbol)
        for symbol in right_hand_symbols:
            if isinstance(symbol, NonTerminal):
                self.non_terminals.add(symbol)
            elif isinstance(symbol, Terminal):
                self.terminals.add(symbol)

    def set_start_symbol(self, symbol: NonTerminal):
        if self.start_symbol is not None:
            raise GrammarError("start symbol already set")
        if symbol not in self.non_terminals:
            raise GrammarError("start symbol is not in non_terminal symbol set of this grammar")

        wrapper_start_symbol = NonTerminal("S'")

        self.add_rule(wrapper_start_symbol, [symbol, EOF])
        self.start_symbol = wrapper_start_symbol

    def check(self):
        if not self.rules:
            raise GrammarError("no rule in grammar")
        if self.start_symbol is None:
            raise GrammarError("no start symbol in grammar")

    def convert_to_nfa(self):
        states = set()
        accepting_states = set()
        stations = {non_terminal: set() for non_terminal in self.non_terminals}

        for rule in self.rules:
            item = RuleItem(0, rule)
            state = LALRNFAState()
            state.items.rule = item
            states.add(state)
            stations[rule.left_hand].add(state)

        for state in list(states):
            current_state = state
            rule = current_state.items.rule.rule
            for dot_pos in range(len(rule.right_hand)):
                link_data = rule.right_hand[dot_pos]

                if isinstance(link_data, NonTerminal):
                    for next_state in stations[link_data]:
                        current_state.link(epsilon, next_state)

                item = RuleItem(dot_pos + 1, rule)
                next_state = LALRNFAState()
                next_state.items.rule = item
                states.add(next_state)
                current_state.link(link_data, next_state)

                current_state = next_state
            if rule.left_hand == self.start_symbol:
                accepting_states.add(current_state)

        start_symbol = self.start_symbol
        start_state = stations[start_symbol].pop()

        return LALRNFA(start_state, accepting_states, states)