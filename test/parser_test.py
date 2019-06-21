from test.output_fsm import output_fsm
from common import Converter, EqualSymbols, DFA

from parser.grammar import Terminal, NonTerminal, Grammar, epsilon
from parser.lalr_nfa import nfa_generator
from parser.channelling import Channelling

t1 = Terminal("t1")
t2 = Terminal("t2")
t3 = Terminal("t3")
NT1 = NonTerminal("NT1")
NT2 = NonTerminal("NT2")
grammar = Grammar("test")
grammar.add_rule(NT1, [NT1, NT2, t3])
grammar.add_rule(NT1, [epsilon, ])
grammar.set_start_symbol(NT1)


nfa = nfa_generator(grammar)
output_fsm(nfa, "LALRNFA")

channeling = Channelling()
channeling.channelling(nfa, grammar)
nfa_eq_symbols = EqualSymbols(nfa)
converter = Converter()
dfa = converter.convert(nfa, nfa_eq_symbols, DFA, "nfa_states")

output_fsm(dfa, "LALRDFA")