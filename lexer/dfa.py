from lexer.helper import epsilon, EOF
from lexer.exceptions import RecognizeError


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
    def __init__(self, start_state, accepting_states, states):
        self.start_state = start_state
        self.accepting_states = accepting_states
        self.states = states
