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

    def display(self):
        print("===== STATE {0} =====".format(self.index))
        state_count = 0
        for symbol in self.connection.keys():
            state = self.connection[symbol]
            print("    link to state {0} with {1}".format(state.index, symbol))
            state_count += 1
        print("TOTAL CONNECTED COUNT: {0}".format(state_count))

    def __repr__(self):
        return "DFAState with id {0}".format(self.index)


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
            sigma.update(state.connection.keys())
        return [{symbol, } for symbol in sigma]

    def display(self):
        all_states = [self.start_state, ]
        index = 0
        while index != len(all_states):
            current_state = all_states[index]
            if current_state is self.start_state:
                print("start state")
            elif current_state in self.accepting_states:
                print("accepting state")
            current_state.display()
            print("\n")
            for next_state in current_state.connection.values():
                if next_state not in all_states:
                    all_states.append(next_state)
            index += 1