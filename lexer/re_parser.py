from abc import abstractmethod
from lexer.helper import StringBuilder, EOF
from lexer.exceptions import RESyntaxError
from lexer.nfa import NFA


class BaseParser:
    def __init__(self, sigma: set):
        self.nfa_class = NFA
        self.sigma = sigma.union({EOF})
        self.sb = StringBuilder(sigma)

        self.regex = None
        self.index = None
        self.re_length = None

    def look_ahead(self):
        if self.index < self.re_length:
            return self.regex[self.index]
        else:
            return EOF

    def consume(self):
        c = self.look_ahead()
        self.index += 1
        return c

    @abstractmethod
    def parse_re(self):
        pass

    def _parse(self):
        nfa = self.parse_re()
        if self.look_ahead() == EOF:
            return nfa
        else:
            raise RESyntaxError()

    def parse(self, regex: str):
        self.regex = list(regex)
        self.re_length = len(regex)
        self.index = 0
        nfa = self._parse()
        return nfa


class REParser(BaseParser):
    """
    _re               ->         re#
    re              ->          concat  (| concat)*
    concat           ->         kleene_closure+

    kleene_closure   ->         atomic* 或者 atomic

    atomic           ->         bracket 或者 parenthesis 或者 letter
    bracket          ->         [range_exp]
        range_exp    ->         略
    parenthesis      ->         (re)
    letter           ->         \escape   |  not_escape | dot
        escape           ->         ESCAPED_SYMBOLS,
        not_escape       ->         不包含META SYMBOLS
        dot              ->         .
    """
    ESCAPES = set("\\")
    META_SYMBOLS = ESCAPES.union(set("[(){*+?|."))
    CONTROL_CHARACTERS = set('nt')
    CONTROL_CHARACTERS_MAPPER = {
        'n': '\n',
        't': '\t',
    }
    ESCAPED_SYMBOLS = META_SYMBOLS.union(CONTROL_CHARACTERS)

    def __init__(self, sigma: set):
        super(REParser, self).__init__(sigma)
        self.first_of_letter = self.sb.not_include(self.META_SYMBOLS).union("\\").union(".")
        self.first_of_atomic = set("[(").union(self.first_of_letter)

    def parse_re(self):
        main_nfa = self.parse_concatenation()

        while self.look_ahead() in  ('|', EOF, ')'):
            if self.look_ahead() == "|":
                self.consume()
                rest_nfa = self.parse_concatenation()
                main_nfa = main_nfa.union(rest_nfa)
            else:
                return main_nfa

        raise RESyntaxError()

    def parse_concatenation(self):
        main_nfa = self.parse_kleene_closure()

        while self.look_ahead() in self.first_of_atomic or self.look_ahead() in ("|", ")", EOF):
            if self.look_ahead() in self.first_of_atomic:
                rest_nfa = self.parse_kleene_closure()
                main_nfa = main_nfa.concat(rest_nfa)
            else:
                return main_nfa

        raise RESyntaxError()

    def parse_kleene_closure(self):
        atomic_exp_nfa = self.parse_atomic()
        if self.look_ahead() == "*":
            self.consume()
            return atomic_exp_nfa.kleene_closure()
        elif self.look_ahead() in self.first_of_atomic or self.look_ahead() in ("|", ")", EOF):
            return atomic_exp_nfa
        else:
            raise RESyntaxError()

    def parse_atomic(self):
        next_symbol = self.look_ahead()
        if next_symbol == '[':
            return self.parse_bracket_exp()
        elif next_symbol == '(':
            return self.parse_parenthesis_exp()
        elif next_symbol in self.first_of_letter:
            return self.parse_letter()
        else:
            raise RESyntaxError()

    def parse_parenthesis_exp(self):
        if self.look_ahead() == '(':
            self.consume()
        else:
            raise RESyntaxError()

        nfa = self.parse_re()

        if self.look_ahead() == ')':
            self.consume()
        else:
            raise RESyntaxError()
        return nfa

    def parse_bracket_exp(self):
        if self.look_ahead() == '[':
            self.consume()
        else:
            raise RESyntaxError()

        nfa = self.parse_one_of_exp()

        if self.look_ahead() == ']':
            self.consume()
        else:
            raise RESyntaxError()
        return nfa

    def parse_one_of_exp(self):
        reverse = False
        if self.look_ahead() == '^':
            self.consume()
            reverse = True
        letters = set(self.parse_letters_in_bracket())
        if reverse:
            letters = self.sb.not_include(letters)

        return self.nfa_class.alter(letters)

    def parse_letters_in_bracket(self) -> str:
        letter = self.parse_letter_in_bracket()
        if self.look_ahead() == '-':
            self.consume()
            return self.parse_letter_range_pairs(letter)
        else:
            return self.parse_letter_set(letter)

    def parse_letter_range_pairs(self, lower_bound) -> str:
        upper_bound = self.parse_letter_in_bracket()
        ranges = [(lower_bound, upper_bound), ]
        while self.look_ahead() != ']':
            lower_bound = self.parse_letter_in_bracket()
            if self.consume() != '-':
                raise RESyntaxError()
            upper_bound = self.parse_letter_in_bracket()
            ranges.append((lower_bound, upper_bound))

        letters = set()
        for pair in ranges:
            lb = ord(pair[0])
            ub = ord(pair[1])
            if lb > ub:
                raise RESyntaxError()
            else:
                for i in range(lb, ub+1):
                    letters.add(chr(i))
        return ''.join(letters)

    def parse_letter_set(self, first_letter) -> str:
        letters = set(first_letter)
        while self.look_ahead() != ']':
            letters.add(self.parse_letter_in_bracket())
        return ''.join(letters)

    def parse_letter_in_bracket(self) -> str:
        if self.look_ahead() == '\\':
            self.consume()
            if self.look_ahead() == '\\' or self.look_ahead() == ']':
                return self.consume()
            else:
                raise RESyntaxError()
        elif self.look_ahead() != ']':
            return self.consume()
        else:
            raise RESyntaxError()

    def parse_letter(self):
        if self.look_ahead() not in self.first_of_letter:
            raise RESyntaxError()
        elif self.look_ahead() in self.ESCAPES:
            self.consume()
            if self.look_ahead() in self.META_SYMBOLS:
                symbol = self.consume()
                return self.nfa_class.alter({symbol})
            elif self.look_ahead() in self.CONTROL_CHARACTERS:
                symbol = self.consume()
                return self.nfa_class.alter({self.CONTROL_CHARACTERS_MAPPER[symbol]})
            else:
                raise RESyntaxError()
        elif self.look_ahead() == '.':
            self.consume()
            letters = self.sb.not_include(set('\n\t'))
            return self.nfa_class.alter(letters)
        else:
            symbol = self.consume()
            return self.nfa_class.alter({symbol})
