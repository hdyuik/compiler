from collections import defaultdict

from .token import Token
from .exceptions import RecognizeError


class ShiftCell:
    def __init__(self, next_state):
        self.next_state = next_state


class ReduceCell:
    def __init__(self, token_type):
        self.token_type = token_type


class ErrorCell:
    def __init__(self):
        pass


class RecognizeTable:
    def __init__(self, dfa):
        self.dfa = dfa
        self.table = defaultdict(dict)
        self.accepting_table = {}
        self.calculate()

    def calculate(self):
        for state in self.dfa.states:
            for edge in state.edges:
                self.table[edge.src_state][edge.symbol] = edge.dest_state
            if state in self.dfa.accepting_states:
                token_types = []
                for nfa_state in state.items.nfa_states:
                    if nfa_state.items.token:
                        token_types.append(nfa_state.items.token)
                token_type = min(token_types, key=lambda t: t.index)
                self.accepting_table[state] = token_type

    def look_up(self, state, symbol):
        try:
            return ShiftCell(self.table[state][symbol])
        except KeyError:
            if state in self.dfa.accepting_states:
                return ReduceCell(self.accepting_table[state])
            else:
                return ErrorCell()

class Recognizer:
    def __init__(self, dfa, key_func):
        self.dfa = dfa
        self.table = RecognizeTable(dfa)
        self.key_func = key_func

    def recognize(self, sentence, index):
        chunk = []
        state = self.dfa.start_state
        while index != len(sentence):
            symbol = self.key_func(sentence[index])
            next_step = self.table.look_up(state, symbol)

            if isinstance(next_step, ShiftCell):
                chunk += sentence[index]
                index += 1
                state = next_step.next_state
            elif isinstance(next_step, ReduceCell):
                token = Token(chunk, next_step.token_type)
                return token
            else:
                raise RecognizeError(self, "can not recognize")


