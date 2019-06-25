from fegen.common import DFAState, DFA


class LALRDFAState(DFAState):
    count = 0


class LALRDFA(DFA):
    StateClass = LALRDFAState
    def minimize(self):
        pass