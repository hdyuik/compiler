from typing import Dict, Set, Any, List
from collections import defaultdict
from functools import reduce

from .symbol import epsilon


class NFAItems:
    def __str__(self):
        res = ""
        for item in self.__dict__.values():
            res += "{0}\n".format(str(item))
        return res


class DFAItems(NFAItems):
    def __init__(self):
        self.nfa_states = set()                                  # type: Set[NFAState]


class Edge:
    def __init__(self, src_state: "NFAState", symbol, dest_state: "NFAState"):
        self.src_state = src_state                                 # type: NFAState
        self.symbol = symbol
        self.dest_state = dest_state                               # type: NFAState


class NFAState:
    count = 0
    ItemStorageClass = NFAItems
    def __init__(self):
        self.__class__.count += 1
        self.index = self.__class__.count
        self.items = self.__class__.ItemStorageClass()             # type: NFAState.ItemStorageClass
        self.edges = []                                            # type: List[Edge]
        self._connection = defaultdict(set)                       # type: Dict[Any, Set[NFAState]]

    def link(self, symbol: Any, state: "NFAState"):
        if symbol not in self._connection or state not in self._connection[symbol]:
            edge = Edge(src_state=self, symbol=symbol, dest_state=state)
            self.edges.append(edge)
            self._connection[symbol].add(state)

    def next(self, symbol) -> List["NFAState"]:
        if symbol in self._connection:
            return list(self._connection[symbol])
        else:
            return []

    def epsilon_closure(self) -> List["NFAState"]:
        result_states = [self, ]
        i = 0
        total = 1
        while i != total:
            for state in result_states[i].next(epsilon):
                if state not in result_states:
                    result_states.append(state)
            i += 1
            total = len(result_states)

        return result_states

    def reach(self, symbol) -> List["NFAState"]:
        end = set()

        start = self.epsilon_closure()
        for state in start:
            end.update(state.next(symbol))

        for state in end.copy():
            end.update(state.epsilon_closure())
        return list(end)

    def __str__(self):
        return "{0} {1}".format(self.__class__.__name__, self.index)


class NFA:
    StateClass = NFAState
    def __init__(self, start_state: NFAState, accepting_states: Set[NFAState], states: Set[NFAState]):
        self.start_state = start_state
        self.accepting_states = accepting_states
        self.states = states

    @property
    def edges(self):
        return reduce(lambda e1, e2: e1 + e2, (state.edges for state in self.states), [])


class DFAState(NFAState):
    count = 0
    ItemStorageClass = DFAItems
    def link(self, symbol, state):
        assert symbol is not epsilon and symbol not in self._connection
        super(DFAState, self).link(symbol, state)

    def epsilon_closure(self) -> List["NFAState"]:
        return []

    def reach(self, symbol) -> List["NFAState"]:
        return self.next(symbol)


class DFA(NFA):
    StateClass = DFAState
    def __init__(self, start_state: DFAState, accepting_states:Set[DFAState], states: Set[DFAState]):
        super(DFA, self).__init__(start_state, accepting_states, states)
        self.minimize()

    def minimize(self):
        # TODO
        pass