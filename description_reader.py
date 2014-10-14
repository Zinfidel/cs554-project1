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
def decodeEscapes(tokens):
    token = tokens[0]
    tokens[0] = token.decode('string_escape') if "\\" in token else token
    return tokens


# Alphabet definition
alphabet_keyword = Keyword("alphabet").suppress()
alphabet_end_keyword = Keyword("end;").suppress() | Keyword("end").suppress()
Symbol = Combine(Literal("\'").suppress() + Optional(Literal("\\")) + \
                 Word(printables + " ", exact=1))
Symbol.setParseAction(decodeEscapes)
SymbolList = OneOrMore(Symbol)
Alphabet = alphabet_keyword + SymbolList + alphabet_end_keyword
# example: ['a, 'b, 'c]

# Regex definition:
RegexSymbol = Combine(Literal("\'") + Optional(Literal("\\")) + \
                      Word(printables + " ", exact=1))
RegexSymbol.setParseAction(decodeEscapes)
Regex = ZeroOrMore(Literal('*') ^
                   Literal('|') ^
                   Literal('+') ^
                   RegexSymbol)
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
Class = class_keyword + identifier + is_keyword + ClassDescription + \
        SemanticRelevance + end_keyword
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
    """Parses the supplied automata file, then constructs and returns an 
       Automata object.

       :param str | file file: File object or URI.
       :rtype: Automata
    """
    fa = FiniteAutomata.parseFile(file)
    # Note on fa.Start: parseResult objects always return values in lists, 
    # so this must be dereferenced.
    return Automata(fa.States, fa.Start[0], fa.Accept, fa.Transitions, \
                    fa.Alphabet)


def ConstructRegex(file):
    """Parses the supplied regex, and constructs the appropriate Regex
       data structure found in ./regex.py
       
       :param str | file file: File object or URI.
       :rtype: Regex
    """
    regex_tokens = Regex.parseString(file)
    return BuildExpression(regex_tokens)


def ConstructLexicalDescription(file):
    """Parses the supplied lexical description file, then constructs and returns
       a lexical description object.

       :param str | file file: File object or URI.
       :rtype: LexicalDesc
    """
    lexDesc = LexicalDescription.parseFile(file)
    return LexicalDesc(lexDesc.Name, lexDesc.Alphabet, lexDesc.Classes)
