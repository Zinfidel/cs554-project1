from automata import Automata
from description_reader import ConstructAutomata
from hopcrofts_algorithm import hopcroftMinimize
from brzozowski import revers, determinis, reachable

file = "testdata/dfa_x.txt"
hop = hopcroftMinimize(file)
#print hop

file2= "testdata/nfa_x.txt"
nfa = ConstructAutomata(file2)
nfa = revers(nfa)
nfa = determinis(nfa)
nfa = reachable(nfa)
nfa = revers(nfa)
nfa = determinis(nfa)
nfa = reachable(nfa)
