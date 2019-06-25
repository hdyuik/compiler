from tests.visualize import output_fsm, output_ast

from compiler_fe import Parser, Grammar, NonTerminal, Terminal, epsilon


def test_json_number():
    minus = Terminal("-")
    plus = Terminal("+")
    one_nine = Terminal("1-9")
    zero = Terminal("0")
    dot = Terminal(".")
    e = Terminal("e")
    upper_e = Terminal("E")

    SIGN = NonTerminal("SIGN")

    INT = NonTerminal("INT")
    DIGITS = NonTerminal("DIGITS")
    DIGIT = NonTerminal("DIGIT")

    FRAC = NonTerminal("FRAC")

    SCI = NonTerminal("SCI")
    SCI_E = NonTerminal("E/e")
    SCI_SIGN = NonTerminal("SCI_SIGN")

    NUMBER = NonTerminal("NUMBER")

    g = Grammar("number")

    g.add_rule(SIGN, [epsilon, ])
    g.add_rule(SIGN, [minus, ])

    g.add_rule(INT, [zero, ])
    g.add_rule(INT, [one_nine, DIGITS, ])
    g.add_rule(DIGITS, [DIGIT, DIGITS, ])
    g.add_rule(DIGITS, [epsilon, ])
    g.add_rule(DIGIT, [zero, ])
    g.add_rule(DIGIT, [one_nine, ])

    g.add_rule(FRAC, [epsilon, ])
    g.add_rule(FRAC, [dot, DIGIT, DIGITS, ])

    g.add_rule(SCI, [epsilon, ])
    g.add_rule(SCI, [SCI_E, SCI_SIGN, DIGIT, DIGITS])
    g.add_rule(SCI_E, [e, ])
    g.add_rule(SCI_E, [upper_e, ])
    g.add_rule(SCI_SIGN, [plus, ])
    g.add_rule(SCI_SIGN, [minus, ])
    g.add_rule(SCI_SIGN, [epsilon, ])

    g.add_rule(NUMBER, [SIGN, INT, FRAC, SCI])

    g.set_start_symbol(NUMBER)

    def key_func(char):
        if char == '-':
            return minus
        elif char in "123456789":
            return one_nine
        elif char == '0':
            return zero
        elif char == '.':
            return dot
        elif char == 'e':
            return e
        elif char == 'E':
            return upper_e
        elif char == '+':
            return plus
    parser = Parser(g, key_func)
    output_fsm(parser.dfa, "LALR_JSON_NUMBER_DFA")

    ast = parser.parse("-145.698e+9")
    output_ast(ast, "LALR_JSON_NUMBER_AST")


def test():
    test_json_number()
    pass

test()