#!/usr/bin/env python

"""description_reader.py: Contains scanner/lexer/tokenizer functions for reading from a file."""

from pyparsing import *
from automata import Automata
from regex import *
from scanner import LexicalDesc

#######################
# General definitions #
#######################
arrow = Keyword("-->").suppress()
end_keyword = Keyword("end;").suppress()

# Alphabet definition
alphabet_keyword = Keyword("alphabet").suppress()
alphabet_end_keyword = Keyword("end;").suppress() | Keyword("end").suppress()
Symbol = Combine(Literal("\'") + Optional(Literal("\\")) + Word(printables + " ", exact=1))
SymbolList = OneOrMore(Symbol)
Alphabet = alphabet_keyword + SymbolList + alphabet_end_keyword
# example: ['a, 'b, 'c]

# Regex definition:
Regex = ZeroOrMore(Literal('*') ^
                   Literal('|') ^
                   Literal('+') ^
                   Symbol)
# example: ['b, +, *, |, 'a, 'o, 'r]


######################
# DFA/NFA definition #
######################
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
FiniteAutomata = automata_keyword \
                 + Group(States).setResultsName("States") \
                 + InitialState.setResultsName("Start") \
                 + Group(AcceptingStates).setResultsName("Accept") \
                 + Group(Transitions).setResultsName("Transitions") \
                 + Group(Alphabet).setResultsName("Alphabet")


###############################
# Complete Lexical Definition #
###############################
identifier = Word(printables)

relevant_keyword = Keyword("relevant")
irrelevant_keyword = Keyword("irrelevant")
discard_keyword = Keyword("discard")
SemanticRelevance = relevant_keyword ^ irrelevant_keyword ^ discard_keyword

ClassDescription = Group(Regex)
# example: ["'b", "'a", "'o", "'r", "'i", "'n", "'g", "' ", "'\\n"]

class_keyword = Keyword("class").suppress()
is_keyword = Keyword("is").suppress()
Class = class_keyword + identifier + is_keyword + ClassDescription + SemanticRelevance + end_keyword
# example: ['base', ['+', "'b", '+', '*', '|', "'a", "'o", "'r"], 'relevant'],

ClassList = ZeroOrMore(Group(Class))

language_keyword = Keyword("language").suppress()
LexicalDescription = language_keyword \
                     + identifier.setResultsName("Name") \
                     + Group(Alphabet).setResultsName("Alphabet") \
                     + Group(ClassList).setResultsName("Classes") \
                     + end_keyword
# example: [z++, [ [class 1], [class 2], [class 3] ] ]


def ConstructAutomata(file):
    """Parses the supplied automata file, then constructs and returns an Automata object.
       The supplied file can either be a file object, or a URI.
    """
    fa = FiniteAutomata.parseFile(file)
    return Automata(fa.States, fa.Start, fa.Accept, fa.Transitions, fa.Alphabet)


def ConstructRegex(file):
    """Parses the supplied regex, and constructs the appropriate Regex data structure found in ./regex.py
       
       The supplied input an be a file object or a URI.
    """
    regex_tokens = Regex.parseString(file)
    return BuildExpression(regex_tokens)


def ConstructLexicalDescription(file):
    """Parses the supplied lexical description file, then constructs and returns a lexical description object.
       The supplied file can either be a file object, or a URI.
    """
    lexDesc = LexicalDescription.parseFile(file)
    return LexicalDesc(lexDesc.Name, lexDesc.Alphabet, lexDesc.Classes)


def BuildExpression(tokens):
    """Builds an expression from a list of tokens using a one token look ahead
       strategy. 

       tokens: Expected to be a list of string tokens (ie: ['+', 'a', 'a'])
    """
    t = tokens[0]

    # E -> + E E
    if t == '+':
        # TODO: Clean this up
        #        return BuildConcatenation(tokens[1:])a
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
    pass