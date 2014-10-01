#!/usr/bin/env python

"""scanner.py: Contains scanner/lexer/tokenizer functions for reading from a file."""

from pyparsing import *
from automata import Automata

# General definitions
arrow = Keyword("-->").suppress()
end_keyword = Keyword("end;").suppress()

# Alphabet definition
alphabet_keyword = Keyword("alphabet").suppress()
alphabet_end_keyword = Keyword("end").suppress()
Symbol = Literal("\'").suppress() + Word(alphas)
SymbolList = OneOrMore(Symbol)
Alphabet = alphabet_keyword + SymbolList + alphabet_end_keyword
# example: ['a, 'b, 'c]

# DFA/NFA definition
states_keyword = Keyword("states").suppress()
State = ~end_keyword + Word(alphanums)
StateList = ZeroOrMore(State)
States = states_keyword + StateList + end_keyword
# example: [s1, s2, s3]

initial_keyword = Keyword("initial").suppress()
InitialState = initial_keyword + State
# example: [s1, s2, s3]

accept_keyword = Keyword("accept").suppress()
AcceptingStates = accept_keyword + StateList + end_keyword
# example: [s1, s2, s3]

transitions_keyword = Keyword("transitions").suppress()
Transition = Group(State + Group(SymbolList) + arrow + State)
TransitionList = ZeroOrMore(Transition)
Transitions = transitions_keyword + TransitionList + end_keyword
# example: [ [s1, ['a, 'b], s2], [s2, ['a], s3] ]

automata_keyword = Keyword("dfa").suppress() ^ Keyword("nfa").suppress()
FiniteAutomata = automata_keyword\
                 + Group(States).setResultsName("States")\
                 + Group(InitialState).setResultsName("Start")\
                 + Group(AcceptingStates).setResultsName("Accept")\
                 + Group(Transitions).setResultsName("Transitions")\
                 + Group(Alphabet).setResultsName("Alphabet")


def ConstructAutomata(file):
    """Parses the supplied automata file, then constructs and returns an Automata object.
       The supplied file can either be a file object, or a URI.
    """
    fa = FiniteAutomata.parseFile(file)
    return Automata(fa.States, fa.Start, fa.Accept, fa.Transitions)

if __name__ == "__main__":
    dfa = ConstructAutomata("testdata/dfa2.txt")
    print dfa.nodes
    print dfa.nodes['s1'].getTransitions(dfa.nodes['s3'])
