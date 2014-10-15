from description_reader import *
from hopcrofts_algorithm import hopcroftMinimize
from brzozowski import convertNfaToMinDfa
from thompsons_construction import convertRegexToNFA
from subset_construction import convertNfaToDfa
from dfa_read import dfa_valid_string


def test_full_toolchain_0():
    """ Tests the full gamut of tools necessary to lex a provided string.
        This test makes use of the following toolchain:
            1) read/lex/generate lexical description data structure
            2) generate regex data structures
            3) use the scanner interface to lex an input file
    """


def test_full_toolchain_1():
    """ Tests the full gamut of tools necessary to validate a provided string.
        This test makes use of the following toolchain:
            1) read/lex/generate lexical description data structure
            2) generate regex data structures
            3) convert regex to nfa
            4) nfa to dfa using subset construction
            5) dfa minimization using Hopcroft's algorithm
            6) validate a string using a dfa
    """
    # Step 1), 2)
    lex_desc = ConstructLexicalDescription("testdata/lexdesc2.txt")

    # Step 3)
    nfa = convertRegexToNFA(lex_desc.classes[3].regex)  # 3 = Integer Arithmetic

    # Step 4)
    dfa = convertNfaToDfa(nfa)

    # Step 5)
    min_dfa = hopcroftMinimize(dfa)

    # Step 6)
    test = True
    test &= dfa_valid_string(min_dfa, "1+3")
    test &= dfa_valid_string(min_dfa, "1-2")
    test &= dfa_valid_string(min_dfa, "3/4")
    test &= dfa_valid_string(min_dfa, "0*3")

    if test:
        print "Toolchain 1: Success!"
    else:
        print "Toolchain 1: Failure!"


def test_full_toolchain_2():
    """ Tests the full gamut of tools necessary to validate a provided string.
        This test makes use of the following toolchain:
            1) read/lex/generate lexical description data structure
            2) generate regex data structures
            3) convert regex to nfa
            4) nfa to minimal dfa using Brzozowki's algorithm
            5) validate a string using a dfa
    """
    # Step 1), 2)
    lex_desc = ConstructLexicalDescription("testdata/lexdesc2.txt")

    # Step 3)
    nfa = convertRegexToNFA(lex_desc.classes[3].regex)  # 3 = Integer Arithmetic

    # Step 4)
    min_dfa = convertNfaToMinDfa(nfa)

    # Step 5)
    test = True
    test &= dfa_valid_string(min_dfa, "1+3")
    test &= dfa_valid_string(min_dfa, "1-2")
    test &= dfa_valid_string(min_dfa, "3/4")
    test &= dfa_valid_string(min_dfa, "0*3")

    if test:
        print "Toolchain2: Success!"
    else:
        print "Toolchain 2: Failure!"

if __name__ == "__main__":
    test_full_toolchain_1()
    test_full_toolchain_2()
