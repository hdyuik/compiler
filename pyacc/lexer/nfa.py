from pyacc.common import NFA, NFAState, NFAItems, epsilon


class LexerNFAItems(NFAItems):
    def __init__(self):
        self.token = None

class LexerNFAState(NFAState):
    ItemStorageClass = LexerNFAItems
    count = 0


class LexerNFA(NFA):
    StateClass = LexerNFAState
    def concat(self, right_nfa: "NFA") -> "NFA":
        new_start_state = LexerNFA.StateClass()
        new_start_state.link(epsilon, self.start_state)

        for accepting_state in self.accepting_states:
            accepting_state.link(epsilon, right_nfa.start_state)

        new_accepting_state = LexerNFA.StateClass()
        for accepting_state in right_nfa.accepting_states:
            accepting_state.link(epsilon, new_accepting_state)
        states = self.states.union(right_nfa.states, [new_start_state, new_accepting_state])

        nfa_data = {
            "start_state": new_start_state,
            "accepting_states": {new_accepting_state, },
            "states": states,
        }
        return LexerNFA(**nfa_data)

    def union(self, right_nfa: "NFA") -> "NFA":
        new_start_state = LexerNFA.StateClass()
        new_start_state.link(epsilon, self.start_state)
        new_start_state.link(epsilon, right_nfa.start_state)

        new_accepting_state = LexerNFA.StateClass()
        for accepting_state in self.accepting_states:
            accepting_state.link(epsilon, new_accepting_state)
        for accepting_state in right_nfa.accepting_states:
            accepting_state.link(epsilon, new_accepting_state)
        states = self.states.union(right_nfa.states).union([new_start_state, new_accepting_state])

        nfa_data = {
            "start_state": new_start_state,
            "accepting_states": {new_accepting_state, },
            "states": states,
        }
        return LexerNFA(**nfa_data)

    def kleene_closure(self) -> "NFA":
        new_start_state = LexerNFA.StateClass()
        new_accepting_state = LexerNFA.StateClass()
        new_start_state.link(epsilon, self.start_state)
        new_start_state.link(epsilon, new_accepting_state)

        for accepting_state in self.accepting_states:
            accepting_state.link(epsilon, new_accepting_state)
            accepting_state.link(epsilon, self.start_state)

        states = self.states.union({new_start_state, new_accepting_state})

        nfa_data = {
            "start_state": new_start_state,
            "accepting_states": {new_accepting_state, },
            "states": states,
        }
        return LexerNFA(**nfa_data)

    def question(self) -> "NFA":
        new_start_state = LexerNFA.StateClass()
        new_accepting_state = LexerNFA.StateClass()
        new_start_state.link(epsilon, new_accepting_state)
        new_start_state.link(epsilon, self.start_state)
        for accepting_state in self.accepting_states:
            accepting_state.link(epsilon, new_accepting_state)

        states = self.states.union([new_start_state, new_accepting_state])
        nfa_data = {
            "start_state": new_start_state,
            "accepting_states": {new_accepting_state, },
            "states": states,
        }
        return LexerNFA(**nfa_data)

    @classmethod
    def one_of(cls, symbols: set) -> "NFA":
        start_state = LexerNFA.StateClass()
        accepting_state = LexerNFA.StateClass()
        for symbol in symbols:
            start_state.link(symbol, accepting_state)

        nfa_data = {
            "start_state": start_state,
            "accepting_states": {accepting_state, },
            "states": {start_state, accepting_state},
        }
        return LexerNFA(**nfa_data)
