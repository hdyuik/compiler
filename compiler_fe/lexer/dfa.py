from compiler_fe.common import DFA, DFAState


class LexerDFAState(DFAState):
    count = 0


class LexerDFA(DFA):
    StateClass = LexerDFAState
