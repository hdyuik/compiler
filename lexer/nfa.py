from common.fsm import NFA, NFAState
from common.symbol import epsilon


class LexerNFAState(NFAState):
    count = 0


class LexerNFA(NFA):
    StateClass = LexerNFAState
    def concat(self, right_nfa: "NFA") -> "NFA":
        for accepting_state in self.accepting_states:
            accepting_state.link(epsilon, right_nfa.start_state)
        accepting_states = right_nfa.accepting_states
        states = set(self.states).union(right_nfa.states)

        nfa_data = {
            "start_state": self.start_state,
            "accepting_states": accepting_states,
            "states": states,
        }
        return LexerNFA(**nfa_data)

    def union(self, right_nfa: "NFA") -> "NFA":
        start_state = LexerNFA.StateClass()
        start_state.link(epsilon, self.start_state)
        start_state.link(epsilon, right_nfa.start_state)
        accepting_states = self.accepting_states.union(right_nfa.accepting_states)
        states = self.states.union(right_nfa.states).union([start_state, ])

        nfa_data = {
            "start_state": start_state,
            "accepting_states": accepting_states,
            "states": states,
        }
        return LexerNFA(**nfa_data)

    def kleene_closure(self) -> "NFA":
        start_state = LexerNFA.StateClass()
        start_state.link(epsilon, self.start_state)
        for accepting_state in self.accepting_states:
            accepting_state.link(epsilon, start_state)
        states = self.states.union({start_state, })

        nfa_data = {
            "start_state": start_state,
            "accepting_states": {start_state, },
            "states": states,
        }
        return LexerNFA(**nfa_data)

    def question(self) -> "NFA":
        nfa_data = {
            "start_state": self.start_state,
            "accepting_states": self.accepting_states.union({self.start_state}),
            "states": self.states,
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
