#!/usr/bin/env python

"""scanner.py: Contains scanner/lexer/tokenizer functions for reading from a file."""

from pyparsing import *

# General definitions
arrow = Keyword("-->")
end_keyword = Keyword("end;")

# Alphabet definition
alphabet_keyword = Keyword("alphabet")
alphabet_end_keyword = Keyword("end")
Symbol = Word("\'", alphas, exact=2)
SymbolList = OneOrMore(Symbol)
Alphabet = alphabet_keyword + SymbolList + alphabet_end_keyword

# DFA/NFA definition
states_keyword = Keyword("states")
State = ~end_keyword + Word(alphanums)
StateList = ZeroOrMore(State)
States = states_keyword + StateList + end_keyword

initial_keyword = Keyword("initial")
InitialState = initial_keyword + State

accept_keyword = Keyword("accept")
AcceptingStates = accept_keyword + StateList + end_keyword

transitions_keyword = Keyword("transitions")
Transition = State + SymbolList + arrow + State
TransitionList = ZeroOrMore(Transition)
Transitions = transitions_keyword + TransitionList + end_keyword

automata_keyword = Keyword("dfa") ^ Keyword("nfa")
Automata = automata_keyword \
           + Group(States)\
           + Group(InitialState)\
           + Group(AcceptingStates)\
           + Group(Transitions)\
           + Group(Alphabet)

print(Automata.parseFile("testdata/dfa2.txt"))