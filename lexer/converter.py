from collections import deque

class Converter:
    def __init__(self, dfa_class):
        self.dfa_class = dfa_class

        self.nfa = None
        self.nfa_accepting_mapper = {}
        self.nfa_symbol_translation = None

        self.dfa_start_state = None
        self.dfa_accepting_mapper = {}
        self.created = {}
        self.pending = deque()

    def pre_configure(self, nfa, nfa_accepting_mapper, nfa_symbol_translation):
        self.nfa = nfa
        self.nfa_accepting_mapper = nfa_accepting_mapper
        self.nfa_symbol_translation = nfa_symbol_translation

        init_nfa_state_set = self.nfa.start_state.closure()
        dfa_start_state = self.new_dfa_state(init_nfa_state_set)

        self.created[init_nfa_state_set] = dfa_start_state
        self.dfa_start_state = dfa_start_state
        self.pending.append(init_nfa_state_set)


    def new_dfa_state(self, nfa_state_set):
        dfa_state = self.dfa_class.StateClass()

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

            for symbol in self.nfa_symbol_translation.sigma:
                des_nfa_states = set()
                for state in src_state_set:
                    des_nfa_states.add(state.reach(symbol))

                link_data = self.nfa_symbol_translation[symbol]

                if des_nfa_states in self.created:
                    old_dfa_state.link(link_data, self.created[des_nfa_states])
                else:
                    new_dfa_state = self.new_dfa_state(des_nfa_states)
                    old_dfa_state.link(link_data, new_dfa_state)
                    self.created[des_nfa_states] = new_dfa_state
                    self.pending.append(des_nfa_states)

    def reset(self):
        self.nfa = None
        self.nfa_accepting_mapper = {}
        self.nfa_symbol_translation = None

        self.dfa_start_state = None
        self.dfa_accepting_mapper.clear()
        self.created.clear()
        self.pending.clear()

    def convert(self, nfa, nfa_accepting_mapper, nfa_symbol_translation):
        self.pre_configure(nfa, nfa_accepting_mapper, nfa_symbol_translation)
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
