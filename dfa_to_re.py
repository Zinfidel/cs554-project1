#!/usr/bin/env python

""" Converts a DFA to a regular expression using Brzozowski's algebraic method.
    http://cs.stackexchange.com/questions/2016/how-to-convert-finite-automata-to-regular-expressions/2017#2017
"""
from regex import *


def __getTransition(dfa, fromStateNum, toStateNum):
    """ Returns transition symbol between the given states, or None if none exists.

        :param Automata dfa: Automata containing the nodes.
        :param int fromStateNum: Index of from state name in dfa.nodes.
        :param int toStateNum: Index of to state name in dfa.nodes.
        :rtype: str | None
    """
    # transState = dfa.nodes[fromState].getTransitionState(symbol)
    # return (transState is not None) and (toState in transState)  # Short-circuit
    fromState = dfa.nodes[dfa.states[fromStateNum]]
    return fromState.getTransitionState()


def __buildArdenSystems(dfa):
    """ Builds the systems of equations A and B in Arden's Lemma:
        X = AX | B  -->  X = A*B

        :param Automata dfa: The DFA to convert to a regular expression.
        :rtype: (list, list)
    """
    m = len(dfa.states)
    stateNumMap = {dfa.states[k]: k for k in range(0, m)}

    # A represents a state transition table for the given DFA.
    A = [[Empty([]) for state in dfa.states] for state in dfa.states]
    for i in range(0, m):
        node = dfa.nodes[dfa.states[i]]
        for symbol in node.transitions.keys():
            for state in node.transitions[symbol]:
                A[i][stateNumMap[state]] = Sigma(symbol)

    # B is a vector of accepting states in the dfa, marked as epsilons.
    B = []
    for i in range(0, m):
        B.append(NilExpression([]) if dfa.nodes[dfa.states[i]].accept else Empty([]))

    return A, B


def convert(dfa):
    """ Converts a DFA into an equivalent regular expression using Brzozowski's Algebraic Method.

        :param Automata dfa: The DFA to convert.
        :rtype: Production
    """
    m = len(dfa.states)
    A, B = __buildArdenSystems(dfa)

    for n in reversed(range(0, m)):
        B[n] = Concatenation(Repetition(A[n][n]), B[n])

        for j in range(0, n):
            A[n][j] = Concatenation(Repetition(A[n][n]), A[n][j])

        for i in range(0, n):
            B[i] = Alternative(B[i], Concatenation(A[i][n], B[n]))

            for j in range(0, n):
                A[i][j] = Alternative(A[i][j], Concatenation(A[i][n], A[n][j]))

    return simplify(B[0])


if __name__ == "__main__":
    from description_reader import ConstructAutomata
    testDFA = ConstructAutomata("testdata/dfa1.txt")
    print convert(testDFA)
