from collections import deque
from lexer.helper import epsilon


class Converter:
    def __init__(self, dfa_state_class, dfa_class):
        self.dfa_state_class = dfa_state_class
        self.dfa_class = dfa_class

        self.nfa = None
        self.nfa_accepting_mapper = None
        self.dfa_start_state = None
        self.dfa_accepting_mapper = {}
        self.created = {}
        self.pending = deque()

    def pre_configure(self, nfa, nfa_accepting_mapper):
        self.nfa = nfa
        self.nfa_accepting_mapper = nfa_accepting_mapper
        init_nfa_state_set = self.nfa.start_state.closure()
        dfa_start_state = self.new_dfa_state(init_nfa_state_set)

        self.created[init_nfa_state_set] = dfa_start_state
        self.dfa_start_state = dfa_start_state
        self.pending.append(init_nfa_state_set)

    def new_dfa_state(self, nfa_state_set):
        dfa_state = self.dfa_state_class()

        token_types = set()
        for state in nfa_state_set:
            if state.index in self.nfa_accepting_mapper:
                token_types.add(self.nfa_accepting_mapper[state.index])

        if token_types:
            self.dfa_accepting_mapper[dfa_state.index] = token_types

        return dfa_state

    def _convert(self):
        while self.pending:
            current = self.pending.popleft()
            src_state_set = current
            old_dfa_state = self.created[src_state_set]

            symbols = set()
            for state in src_state_set:
                symbols.add(*state.connection.keys())
            symbols.remove(epsilon)

            if symbols:
                for symbol in symbols:
                    des_nfa_states = set()
                    for state in src_state_set:
                        des_nfa_states.add(state.reach(symbol))
                    if des_nfa_states in self.created:
                        old_dfa_state.link(symbol, self.created[des_nfa_states])
                    else:
                        new_dfa_state = self.new_dfa_state(des_nfa_states)
                        old_dfa_state.link(symbol, new_dfa_state)
                        self.created[des_nfa_states] = new_dfa_state
                        self.pending.append(des_nfa_states)

    def reset(self):
        pass

    def convert(self, nfa, nfa_accepting_mapper):
        self.pre_configure(nfa, nfa_accepting_mapper)
        self._convert()
        dfa_construction_data = {
            "start_state": self.dfa_start_state,
            "accepting_states": set(self.dfa_accepting_mapper.keys()),
            "states": set(self.created.values()),
        }
        dfa = self.dfa_class(**dfa_construction_data)
        dfa_accepting_mapper = self.dfa_accepting_mapper
        self.reset()
        return {
            "dfa": dfa,
            "accepting_mapper": dfa_accepting_mapper,
        }
