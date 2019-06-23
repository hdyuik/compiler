import warnings
from collections import defaultdict

from common import epsilon
from parser.exceptions import AnalyzeError
from parser.ast import AST, Leaf
from parser.lalr_dfa import LALRDFA


class ReduceCell:
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return "reduce using rule {0}".format(self.rule)

class ShiftCell:
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return "shift to state{0}".format(self.state.index)

class ErrorCell:
    def __init__(self):
        pass

error_cell = ErrorCell()

class LALRParsingTable:
    def __init__(self, lalr_dfa: LALRDFA):
        self.dfa = lalr_dfa
        self.table = None
        self.calculate()

    def calculate(self):
        table = defaultdict(dict)

        for state in self.dfa.states:
            for edge in state.edges:
                table[state.index][edge.symbol] = ShiftCell(edge.dest_state)
            for nfa_state in state.items.nfa_states:
                rule_item = nfa_state.items.rule
                if rule_item.reduce():
                    for symbol in nfa_state.items.look_ahead.symbols:
                        table[state.index][symbol] = ReduceCell(rule_item.rule)
        self.table = table

    def look_up(self, state_index, symbol):
        try:
            return self.table[state_index][symbol]
        except KeyError:
            return error_cell


class LALRAnalyzer:
    epsilon_leaf = Leaf(epsilon, "ε")
    def __init__(self, lalr_dfa, key_func):
        self.lalr_dfa = lalr_dfa
        self.table = LALRParsingTable(self.lalr_dfa)
        self.key_func = key_func

        self._parsing_stack = []
        self._inputs = []

    def look_ahead(self):
        symbol = self._inputs[-1].root_symbol
        state_index = self._parsing_stack[-1].index
        next_step = self.table.look_up(state_index, symbol)
        if isinstance(next_step, ShiftCell):
            self.shift(next_step.state)
        elif isinstance(next_step, ReduceCell):
            self.reduce(next_step.rule)
        else:
            raise AnalyzeError(self, 'error')

    def reduce(self, rule):
        children = []
        if epsilon in rule.right_hand:
            children.append(self.epsilon_leaf)
        else:
            for i in range(2 * len(rule.right_hand)):
                thing = self._parsing_stack.pop()
                if i % 2 != 0:
                    children.insert(0, thing)
        ast = AST(rule.left_hand, rule, *children)
        self._inputs.append(ast)

    def shift(self, state):
        ast = self._inputs.pop()
        self._parsing_stack.append(ast)
        self._parsing_stack.append(state)

    def reset(self):
        self._inputs = []
        self._parsing_stack = []

    def analyze(self, inputs):
        if len(inputs) == 0:
            raise AnalyzeError(self, "empty input")

        for thing in reversed(inputs):
            symbol = self.key_func(thing)
            if symbol is None:
                warnings.warn("input covert to None via key_func, something could be wrong")
            leaf = Leaf(symbol, thing)
            self._inputs.append(leaf)

        self._parsing_stack.append(self.lalr_dfa.start_state)
        while self._inputs:
            self.look_ahead()

        final_state = self._parsing_stack[-1]
        if final_state in self.lalr_dfa.accepting_states:
            children = []
            for i in range(len(self._parsing_stack)):
                thing = self._parsing_stack.pop()
                if i % 2 != 0:
                    children.insert(0, thing)
            self.reset()
            return children
        else:
            self.reset()
            raise AnalyzeError(self, "can not parse")