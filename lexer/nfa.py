from typing import Set, Dict, Any
from lexer.helper import epsilon


class NFAState:
    count = 0
    def __init__(self):
        NFAState.count += 1
        self.index = NFAState.count
        self.connection = {}    # type: Dict[Any, Set[NFAState]]

    def link(self, symbol, state):
        if symbol in self.connection:
            self.connection[symbol].add(state)
        else:
            target_state = set()
            target_state.add(state)
            self.connection[symbol] = target_state

    def reach(self, symbol):
        start = self.closure()
        end = set()
        for state in start:
            if symbol in state.connection:
                end.update(state.connection[symbol])

        for state in end:
            end.update(state.closure())
        return end

    def closure(self):
        result_states = set()
        result_states.add(self)
        if epsilon in self.connection:
            direct_states = self.connection[epsilon]
            for state in direct_states:
                result_states.update(state.closure())

        return result_states

    def display(self):
        print("===== STATE {0} =====".format(self.index))
        state_count = 0
        for symbol in self.connection.keys():
            for state in self.connection[symbol]:
                print("    link to state {0} with {1}".format(state.index, symbol))
                state_count += 1
        print("TOTAL CONNECTED COUNT: {0}".format(state_count))


class NFA:
    def __init__(self, start_state: NFAState, accepting_states: Set[NFAState], all_states: Set[NFAState]):
        self.states = all_states
        self.start_state = start_state
        self.accepting_states = accepting_states

    def concat(self, right_nfa: "NFA") -> "NFA":
        for accepting_state in self.accepting_states:
            accepting_state.link(epsilon, right_nfa.start_state)

        accepting_states = right_nfa.accepting_states
        all_states = set(self.states).union(right_nfa.states)
        return NFA(self.start_state, accepting_states, all_states)

    def union(self, right_nfa: "NFA") -> "NFA":
        start_state = NFAState()
        start_state.link(epsilon, self.start_state)
        start_state.link(epsilon, right_nfa.start_state)

        accepting_states = self.accepting_states.union(right_nfa.accepting_states)
        all_states = self.states.union(right_nfa.states).union([start_state, ])
        return NFA(start_state, accepting_states, all_states)

    def kleene_closure(self) -> "NFA":
        start_state = NFAState()
        start_state.link(epsilon, self.start_state)
        for accepting_state in self.accepting_states:
            accepting_state.link(epsilon, start_state)

        all_states = self.states.union({start_state, })

        return NFA(start_state, {start_state}, all_states)

    @classmethod
    def alter(cls, symbols: set) -> "NFA":
        start_state = NFAState()
        accepting_state = NFAState()
        for symbol in symbols:
            start_state.link(symbol, accepting_state)

        return NFA(start_state, {accepting_state, }, {start_state, accepting_state})

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
            for linked_state_s in current_state.connection.values():
                for next_state in linked_state_s:
                    if next_state not in all_states:
                        all_states.append(next_state)

            index += 1