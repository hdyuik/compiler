from typing import Set, Dict, Any, List
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

    def closure(self) -> Set["NFAState"]:
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
    StateClass = NFAState
    def __init__(self, start_state: NFAState, accepting_states: Set[NFAState], states: Set[NFAState], cb: List[Set[Any]], icb: Set[Any]):
        self.states = states
        self.start_state = start_state
        self.accepting_states = accepting_states

        self.cb = cb
        self.icb = icb

    def concat(self, right_nfa: "NFA") -> "NFA":
        for accepting_state in self.accepting_states:
            accepting_state.link(epsilon, right_nfa.start_state)
        accepting_states = right_nfa.accepting_states
        states = set(self.states).union(right_nfa.states)
        cb, icb = self.calculate_compression(self.cb, self.icb, right_nfa.cb, right_nfa.icb)

        nfa_data = {
            "start_state": self.start_state,
            "accepting_states": accepting_states,
            "states": states,
            "cb": cb,
            "icb": icb,
        }
        return NFA(**nfa_data)

    def union(self, right_nfa: "NFA") -> "NFA":
        start_state = NFA.StateClass()
        start_state.link(epsilon, self.start_state)
        start_state.link(epsilon, right_nfa.start_state)
        accepting_states = self.accepting_states.union(right_nfa.accepting_states)
        states = self.states.union(right_nfa.states).union([start_state, ])
        cb, icb = self.calculate_compression(self.cb, self.icb, right_nfa.cb, right_nfa.icb)

        nfa_data = {
            "start_state": start_state,
            "accepting_states": accepting_states,
            "states": states,
            "cb": cb,
            "icb": icb,
        }
        return NFA(**nfa_data)

    def kleene_closure(self) -> "NFA":
        start_state = NFA.StateClass()
        start_state.link(epsilon, self.start_state)
        for accepting_state in self.accepting_states:
            accepting_state.link(epsilon, start_state)
        states = self.states.union({start_state, })

        nfa_data = {
            "start_state": start_state,
            "accepting_states": {start_state, },
            "states": states,
            "cb": self.cb,
            "icb": self.icb,
        }
        return NFA(**nfa_data)

    def question(self) -> "NFA":
        nfa_data = {
            "start_state": self.start_state,
            "accepting_states": self.accepting_states.union({self.start_state}),
            "states": self.states,
            "cb": self.cb,
            "icb": self.icb,
        }
        return NFA(**nfa_data)

    @classmethod
    def one_of(cls, symbols: set) -> "NFA":
        start_state = NFA.StateClass()
        accepting_state = NFA.StateClass()
        for symbol in symbols:
            start_state.link(symbol, accepting_state)

        nfa_data = {
            "start_state": start_state,
            "accepting_states": {accepting_state, },
            "states": {start_state, accepting_state},
            "cb": [symbols, ],
            "icb": set(),
        }
        return NFA(**nfa_data)

    @staticmethod
    def calculate_compression(left_compressible: List[Set[Any]], left_incompressible: Set[Any],
                              right_compressible: List[Set[Any]], right_incompressible: Set[Any]):
        print("cal")
        left_cb = [compressible_set.difference(right_incompressible) for compressible_set in left_compressible]
        right_cb = [compressible_set.difference(left_incompressible) for compressible_set in right_compressible]
        icb = left_incompressible.union(right_incompressible)
        cb = []

        for left_set in left_cb:
            for right_set in right_cb:
                intersection = left_set.intersection(right_set)
                cb.append(intersection)
                left_set.difference_update(intersection)
                right_set.difference_update(intersection)
        cb.extend(left_cb)
        cb.extend(right_cb)

        discard = [cb_set for cb_set in cb if len(cb_set) in (0, 1)]
        for obj in discard:
            cb.remove(obj)
            icb.update(obj)

        return cb, icb

    @property
    def compact_symbol_sets(self):
        compression = [{char, } for char in self.icb]
        compression.extend(self.cb)
        return compression

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