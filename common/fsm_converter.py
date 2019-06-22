from collections import deque


class ConvertItem(set):
    def __str__(self):
        return "NFAStates: {0}".format(" ".join(str(state.index) for state in self))

class Converter:
    def __init__(self):
        self.dfa_class = None
        self.nfa = None
        self.eq_symbol_set = None
        self.dfa_start_state = None
        self.dfa_accepting_states = None
        self.created = None
        self.pending = None
        self.item_attr_name = None

    @staticmethod
    def sorted_state_indexes(state_set):
        return tuple(state.index for state in sorted(state_set, key=lambda state: state.index))

    def pre_configure(self, nfa, eq_symbols, dfa_class, item_attr_name):
        self.nfa = nfa
        self.dfa_class = dfa_class
        self.eq_symbol_set = eq_symbols
        self.dfa_accepting_states = set()
        self.created = {}
        self.pending = deque()
        self.item_attr_name = item_attr_name

        init_nfa_state_set = self.nfa.start_state.epsilon_closure()
        state_indexes = self.sorted_state_indexes(init_nfa_state_set)
        dfa_start_state = self.new_dfa_state(init_nfa_state_set)

        self.created[state_indexes] = dfa_start_state
        self.dfa_start_state = dfa_start_state
        self.pending.append(dfa_start_state)

    def new_dfa_state(self, nfa_state_set):
        dfa_state = self.dfa_class.StateClass()
        setattr(dfa_state.items, self.item_attr_name, ConvertItem(nfa_state_set))
        return dfa_state

    def _convert(self):
        while self.pending:
            src_dfa_state = self.pending.popleft()
            for symbol in self.eq_symbol_set.sigma:
                des_nfa_states = set()
                for src_nfa_state in getattr(src_dfa_state.items, self.item_attr_name):
                    des_nfa_states.update(src_nfa_state.reach(symbol))
                if des_nfa_states:
                    link_data = self.eq_symbol_set.index(symbol)

                    indexes = self.sorted_state_indexes(des_nfa_states)
                    if indexes in self.created:
                        src_dfa_state.link(link_data, self.created[indexes])
                    else:
                        new_dfa_state = self.new_dfa_state(des_nfa_states)
                        src_dfa_state.link(link_data, new_dfa_state)

                        self.created[indexes] = new_dfa_state
                        self.pending.append(new_dfa_state)
                        for state in des_nfa_states:
                            if state in self.nfa.accepting_states:
                                self.dfa_accepting_states.add(new_dfa_state)

    def reset(self):
        self.dfa_class = None
        self.nfa = None
        self.eq_symbol_set = None
        self.dfa_start_state = None
        self.dfa_accepting_states = None
        self.created = None
        self.pending = None
        self.item_attr_name = None

    def convert(self, nfa, eq_symbols, dfa_class, item_attr_name="nfa_states"):
        self.pre_configure(nfa, eq_symbols, dfa_class, item_attr_name)
        self._convert()
        dfa_construction_data = {
            "start_state": self.dfa_start_state,
            "accepting_states": self.dfa_accepting_states,
            "states": set(self.created.values()),
        }
        dfa = self.dfa_class(**dfa_construction_data)
        self.reset()
        return dfa
