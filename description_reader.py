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
    # Alphabet check: if there are symbols in the transitions not in the
    # alphabet, throw an exception.
    for trans in fa.Transitions:
        for symbol in trans[1]:
            if symbol not in fa.Alphabet.asList():
                trans_str = trans[0] + ' \''\
                            + " \'".join(trans[1])\
                            + " --> " + trans[2]
                raise Exception("Alphabet Error! The transition:\n\n"\
                                + "    " + trans_str + "\n\n"\
                                + " contains the symbol \'" + symbol + "\' "\
                                + "which is not in the described alphabet!")

    # Note on fa.Start: parseResult objects always return values in lists,
    # so this must be dereferenced.
    return Automata(fa.States, fa.Start[0], fa.Accept, fa.Transitions,\
                    fa.Alphabet)



def ConstructLexicalDescription(file):
    """Parses the supplied lexical description file, then constructs and returns
       a lexical description object.

       :param str | file file: File object or URI.
       :rtype: LexicalDesc
    """
    lexDesc = LexicalDescription.parseFile(file)

    # Alphabet check: if there are symbols in the regexes defined in this
    # lexical description that aren't in the alphabet, raise an exception.
    for clazz in lexDesc.Classes:
        for symbol in clazz[1]:
            if (len(symbol) > 1) and (symbol[1:] not in lexDesc.Alphabet.asList()):
                regex_str = ' '.join(clazz[1])
                raise Exception("Alphabet Error! The regex:\n\n" \
                                + "    " + regex_str + "\n\n" \
                                + " contains the symbol \'" + symbol[1:] + "\' " \
                                + "which is not in the described alphabet!")


    return LexicalDesc(lexDesc.Name, lexDesc.Alphabet, lexDesc.Classes)


if __name__ == "__main__":
    lex_desc = ConstructLexicalDescription("./testdata/tiny_basic_lex_desc.txt")
    tbProgram = open('./testdata/tinyBasicProgram.txt').read()
    print lex_desc.scan(tbProgram)
