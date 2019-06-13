from lexer.re_parser import REParser


parser = REParser(set([chr(code) for code in range(256)]))


def test_concat():
    nfa = parser.parse("abcnf")
    nfa.display()

def test_union():
    nfa = parser.parse("ac|bf")
    nfa.display()

def test_kleene_closure():
    nfa = parser.parse("ab*")
    nfa.display()

def test_parenthesis():
    nfa = parser.parse("abc(d|f)*")
    nfa.display()

def test_bracket1():
    nfa = parser.parse("hell[oaf]")
    nfa.display()

def test_bracket2():
    nfa = parser.parse("hell[c-kE-Z]")  # c-kE-Z  总计31个字符
    nfa.display()

def test_bracket3():
    nfa = parser.parse("hell[^c-kE-Z]")
    nfa.display()

def test():
    # test_concat()
    # test_union()
    # test_kleene_closure()
    # test_parenthesis()
    # test_bracket1()
    # test_bracket2()
    # test_bracket3()
    pass

test()
