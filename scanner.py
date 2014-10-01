#!/usr/bin/env python

"""scanner.py: Contains scanner/lexer/tokenizer functions for reading from a file."""

from pyparsing import *
from automata import Automata
from regex import *

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


# Regex parsing:
Regex = ZeroOrMore(Literal('*') | \
                   Literal('|') | \
                   Literal('+') | \
                   Symbol)

def ConstructRegex(file):
    '''Parses the supplied regex, and constructs the appropriate Regex data structure found in ./regex.py
       
       The supplied input an be a file object or a URI.
    '''
    regex_tokens = Regex.parseFile(file)
    r, leftover = BuildExpression(regex_tokens)
    pass

def BuildExpression(tokens):
    '''Builds an expression from a list of tokens using a one token look ahead
       strategy. 

       tokens: Expected to be a list of string tokens (ie: ['+', 'a', 'a'])
    '''
    t = tokens[0]

    # E -> + E E
    if t == '+':
        # build the appropriate expression for the left argument to the concat
        # operation and return the leftover tokens
        leftSide, leftover = BuildExpression(tokens[1:])
       
        # Make sure we have tokens to consume, otherwise an error
        if len(leftover) == 0:
            raise Error('''No more tokens found after building the left hand side of
                           a ConcatExpression''')
        # Build the right hand side of the ConcatExpression
        rightSide, leftover = BuildExpression(leftover)
        return Concatenation(leftSide, rightSide), leftover
    # E -> | E E
    elif t == '|':

        leftSide, leftover = BuildExpression(tokens[1:])

        # Make sure we have tokens to consume, otherwise an error
        if len(leftover) == 0:
            raise Error('''No more tokens found after building the left hand side of
                           a ConcatExpression''')

        rightSide, leftover = BuildExpression(leftover)
        return Alternative(leftSide, rightSide), leftover
    # E -> * E
    elif t == '*':
        e, leftover = BuildExpression(tokens[1:])
        return Repetition(e), leftover
    # E -> _ (empty, not underscore)
    elif t == '':
        return NilExpression(), tokens[1:]
    # E -> sigma (where sigma is some symbol that doesn't match the previous
    # values
    else:
        return Sigma(t), tokens[1:]
        


if __name__ == "__main__":
    tokens = Regex.parseString("+ 'a 'a")
    print tokens
    e, l = BuildExpression(tokens)
    print e
    print l
#    print Symbol.parseString('\' ') # <---- TODO: This should work... ' ' can
                                    #             be part of the alphabet
