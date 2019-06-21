from common.fsm import DFA, DFAState


class LexerDFAState(DFAState):
    count = 0

    def display(self):
        print("===== STATE {0} =====".format(self.index))
        state_count = 0
        for edge in self.edges:
            print("    link  to state {0} with {1}".format(edge.dest_state.index, edge.symbol))
            state_count += 1
        print("TOTAL CONNECTED COUNT: {0}".format(state_count))


class LexerDFA(DFA):
    StateClass = LexerDFAState

    def display(self):
        for state in self.states:
            if state is self.start_state:
                print("START")
            elif state in self.accepting_states:
                print("ACCEPTING")
            state.display()
            print("\n")