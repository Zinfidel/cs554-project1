#!/usr/bin/env python
#ok, this is a testing thingy- justin
#test 2

"""scanner.py: Contains scanner/lexer/tokenizer functions for reading from a file."""

from pyparsing import *

# General definitions
arrow = Keyword("-->").suppress()
end_keyword = Keyword("end;").suppress()

# Alphabet definition
alphabet_keyword = Keyword("alphabet").suppress()
alphabet_end_keyword = Keyword("end").suppress()
#Symbol = Word("\'", alphas, exact=2)
Tick = Keyword("\'")
Symbol = Keyword("\'") + (~Keyword('\n') + Word(alphas))
SymbolList = OneOrMore(Symbol) + Keyword('\n')
#SymbolList = OneOrMore(Symbol)
Alphabet = alphabet_keyword + SymbolList + alphabet_end_keyword

# DFA/NFA definition
states_keyword = Keyword("states").suppress()
State = ~end_keyword + Word(alphanums)
StateList = ZeroOrMore(State)
States = states_keyword + StateList + end_keyword

initial_keyword = Keyword("initial").suppress()
InitialState = initial_keyword + State

accept_keyword = Keyword("accept").suppress()
AcceptingStates = accept_keyword + StateList + end_keyword

transitions_keyword = Keyword("transitions").suppress()
Transition = State + SymbolList + arrow + State
TransitionList = ZeroOrMore(Transition)
Transitions = transitions_keyword + TransitionList + end_keyword

automata_keyword = Keyword("dfa").suppress() ^ Keyword("nfa").suppress()
Automata = automata_keyword \
           + Group(States)\
           + Group(InitialState)\
           + Group(AcceptingStates)\
           + Group(Transitions)\
           + Group(Alphabet)

def ParseAutomata(charList):
    return {idx:x for (idx,x) in enumerate(Automata.parseString(charList))}

def ConstructAutomata(charList):
    rawAutomata = ParseAutomata(charList)

    statesList = rawAutomata[AutomataTokenDictionary["States"]]
    startStatesList = rawAutomata[AutomataTokenDictionary["Start"]]
    acceptStatesList = rawAutomata[AutomataTokenDictionary["Accept"]]
    transitionsList = rawAutomata[AutomataTokenDictionary["Transitions"]]
    sigma = rawAutomata[AutomataTokenDictionary["Alphabet"]]

    print "Sigma: ", sigma
    print "States: ", statesList
    print "Start States: ", startStatesList
    for s in transitionsList:
        print "Transition: ", s


AutomataTokenDictionary = {y:x for (x,y) in enumerate(["States", "Start", "Accept", "Transitions", "Alphabet"])}
#print {idx:x for (idx,x) in enumerate(Automata.parseFile("testdata/dfa2.txt"))}


if __name__ == "__main__":
#    print OneOrMore(Word(alphas)).setDebug().parseString("asdfa asd dkjlasdf dsf")
    print SymbolList.parseString("'a 'b 'c\n'")
#    ConstructAutomata(open("testdata/dfa2.txt").read())
