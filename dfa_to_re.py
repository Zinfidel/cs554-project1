#!/usr/bin/env python

""" Converts a DFA to a regular expression using Brzozowski's algebraic method.
    http://cs.stackexchange.com/questions/2016/how-to-convert-finite-automata-to-regular-expressions/2017#2017
"""

from automata import *
from regex import *

EPSILON = '\0'


def __getTransition(dfa, fromStateNum, toStateNum):
    """ Returns transition symbol between the given states, or None if none exists.

        :param Automata dfa: Automata containing the nodes.
        :param str fromStateNum: Index of from state name in dfa.nodes.
        :param str toStateNum: Index of to state name in dfa.nodes.
        :rtype: str | None
    """
    # transState = dfa.nodes[fromState].getTransitionState(symbol)
    # return (transState is not None) and (toState in transState)  # Short-circuit
    fromState = dfa.nodes[dfa.states[fromStateNum]]
    return fromState.getTransitionState()


def buildArdenSystems(dfa):
    """ Builds the systems of equations A and B in Arden's Lemma:
        X = AX | B  -->  X = A*B

        :param Automata dfa: The DFA to convert to a regular expression.
        :rtype: (list, list)
    """

    m = len(dfa.states)
    stateNumMap = {dfa.states[k]: k for k in range(0, m)}

    # A represents a state transition table for the given DFA.
    A = [[None for state in dfa.states] for state in dfa.states]
    for i in range(0, m):
        node = dfa.nodes[dfa.states[i]]
        for symbol in node.transitions.keys():
            for state in node.transitions[symbol]:
                A[i][stateNumMap[state]] = symbol

    # B is a vector of accepting states in the dfa, marked as epsilons.
    B = []
    for i in range(0, m):
        B.append(EPSILON if dfa.nodes[dfa.states[i]].accept else None)

    return A, B

if __name__ == "__main__":
    from description_reader import ConstructAutomata
    testDFA = ConstructAutomata("testdata/dfa1.txt")
    # print __hasTransition(testDFA, "blah1", "blah2", 'a')
    # print __hasTransition(testDFA, "blah1", "blah2", 'b')
    a, b = buildArdenSystems(testDFA)
    print a
    print b
