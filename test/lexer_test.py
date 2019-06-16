from lexer.nfa import NFA
from lexer.re_parser import REParser
from lexer.converter import Converter
from lexer.dfa import DFA
from lexer.symbol_translation import SymbolTranslation
from lexer.token import TokenType

parser = REParser(NFA)
converter = Converter(DFA)

def get_accepting_mapper(nfa, token):
    nfa_accepting_mapper = {}
    for state in nfa.accepting_states:
        nfa_accepting_mapper[state] = token
    return nfa_accepting_mapper


def get_fa_translation(fa):
    nfa_symbol_translation = SymbolTranslation()
    for index, symbol_set in enumerate(fa.compact_symbol_sets):
        for symbol in symbol_set:
            nfa_symbol_translation[symbol] = index+1
    return nfa_symbol_translation


def test_json_number():
    token = TokenType("json number", "-?(0|[1-9][0-9]*)(\\.[0-9][0-9]*)?([eE][-+]?[0-9][0-9]*)?")
    nfa = parser.parse(token.regex)
    nfa_translation = get_fa_translation(nfa)
    nfa_accepting_mapper = get_accepting_mapper(nfa, token)
    result = converter.convert(nfa, nfa_accepting_mapper, nfa_translation)
    print("================== nfa ==================")
    # nfa.display()
    print("nfa symbol translation: ", nfa_translation)
    print("nfa accepting mapper", nfa_accepting_mapper)

    dfa = result['dfa']
    accepting_mapper = result['accepting_mapper']
    dfa_translation = get_fa_translation(dfa)
    print("================== nfa ==================")
    # dfa.display()
    print("dfa symbol translation", dfa_translation)
    print("dfa accepting mapper", accepting_mapper)

    final_translation = nfa_translation.concat(get_fa_translation(dfa))
    print("final translation: ", final_translation)


def test_json_string():
    control_characters = ''.join([chr(i) for i in range(32)])
    control_characters += chr(127)
    token = TokenType("json string", r'"([^"\\{0}]|\\["\\/bfnrtu])*"'.format(control_characters))
    nfa = parser.parse(token.regex)
    nfa_translation = get_fa_translation(nfa)
    nfa_accepting_mapper = get_accepting_mapper(nfa, token)
    result = converter.convert(nfa, nfa_accepting_mapper, nfa_translation)
    print("================== nfa ==================")
    # nfa.display()
    print("nfa symbol translation: ", nfa_translation)
    print("nfa accepting mapper", nfa_accepting_mapper)

    dfa = result['dfa']
    accepting_mapper = result['accepting_mapper']
    dfa_translation = get_fa_translation(dfa)
    print("================== nfa ==================")
    dfa.display()
    print("dfa symbol translation", dfa_translation)
    print("dfa accepting mapper", accepting_mapper)

    final_translation = nfa_translation.concat(get_fa_translation(dfa))
    print("final translation: ", final_translation)

def test():
    # test_json_number()
    test_json_string()
    pass

test()
