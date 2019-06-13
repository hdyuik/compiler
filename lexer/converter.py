from functools import reduce
from collections import deque
from lexer.helper import StringBuilder


class Converter:
    def __init__(self, dfa_state_class, sigma):
        self.sb = StringBuilder(sigma)
        self.dfa_state_class = dfa_state_class

    def convert(self, nfas_tokens):
        accepting_state_record = {}
        for nfa, token_id in nfas_tokens:
            for accepting_state in nfa.accepting_states:
                accepting_state_record[accepting_state] = token_id

        pending = deque()
        created = {}
        whole_nfa = reduce(lambda nfa1, nfa2: nfa.union(nfa2), [nfa for nfa, token in nfas_tokens])
        init_nfa_state_s = whole_nfa.start_state.closure()
        init_dfa_state = self.make_dfa_state(init_nfa_state_s, accepting_state_record)

        pending.append(init_nfa_state_s)
        created[init_nfa_state_s] = init_dfa_state

        while pending:
            current = pending.popleft()
            src_state_s = current[0]
            old_state = created[src_state_s]
            for symbol in self.sb.sigma:
                des_states = set()
                for src_nfa_state in src_state_s:
                    des_states.add(src_nfa_state.move(symbol))
                if des_states:
                    if des_states in created:
                        old_state.link(symbol, created[des_states])
                    else:
                        new_state = self.make_dfa_state(des_states, accepting_state_record)
                        old_state.link(symbol, new_state)
                        created[des_states] = new_state
                        pending.append(des_states)
        return init_dfa_state

    def make_dfa_state(self, nfa_states, accepting_state_record):
        dfa_state = self.dfa_state_class()

        token_ids = set()
        for state in nfa_states:
            if state in accepting_state_record:
                token_ids.add(accepting_state_record[state])

        if token_ids:
            dfa_state.set_token_id(min(token_ids))

        return dfa_state