from typing import Set
from lexer.helper import epsilon


class DFAState:
    count = 0
    def __init__(self):
        DFAState.count += 1
        self.index = DFAState.count
        self.connection = {}

    def link(self, symbol, state):
        assert symbol not in self.connection and symbol is not epsilon
        self.connection[symbol] = state


class DFA:
    StateClass = DFAState
    def __init__(self, start_state: DFAState, accepting_states:Set[DFAState], states: Set[DFAState]):
        self.start_state = start_state
        self.accepting_states = accepting_states
        self.states = states
        self.minimize()

    def minimize(self):
        pass

    @property
    def compact_symbol_sets(self):
        sigma = set()
        for state in self.states:
            sigma.union(state.connection.keys())
        return sigma