from lexer.helper import epsilon, EOF
from lexer.exceptions import RecognizeError


class DFAState:
    count = 0
    def __init__(self):
        DFAState.count += 1
        self.index = DFAState.count
        self.connection = {}
        self._token_id = None

    def link(self, symbol, state):
        assert symbol not in self.connection and symbol is not epsilon
        self.connection[symbol] = state

    @property
    def token_id(self):
        return self._token_id

    @token_id.setter
    def token_id(self, token_id):
        self._token_id = token_id

    @property
    def is_accepting(self):
        return self.token_id is not  None


class DFA:
    def __init__(self, start_state):
        self.init_state = start_state
        self.current_state = start_state
        self.saved = ""

    def accept(self, symbol):
        if symbol in self.current_state.connection:
            self.saved += symbol
            self.current_state = self.current_state.connection[symbol]
            return True
        else:
            return False

    def in_accepting(self):
        return self.current_state.is_accepting()

    def current_token_id(self):
        assert self.in_accepting()
        return self.current_state.token_id

    def reset(self):
        self.current_state = self.init_state
        self.saved = ""

    def recognize(self, input_str):
        input_string = list(input_str) + [EOF, ]
        index = 0
        ret = []
        while index != len(ret):
            symbol = input_string[index]
            if self.accept(symbol):
                index += 1
            else:
                if self.in_accepting():
                    chunk = (self.saved, self.current_token_id())
                    ret.append(chunk)
                    self.reset()
                else:
                    raise RecognizeError()
        return ret
