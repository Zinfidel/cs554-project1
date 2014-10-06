from automata import *

EPSILON = '\0'


def epsilonClosure(state, visitedStates, nfa):
    """ Calculates the epsilon closure over a state. In English, this
        function returns the set of all states reachable via epsilon-transitions
        from the initially provided state. Note that this returned set will
        include the original state as any state can reach itself via an epsilon-
        transition. This function can traverse over multiple epsilon transitions
        and thus can return states further than one transition.

        :param AutomataNode state: Initial state.
        :param set[AutomataNode] visitedStates: Set of states already visited.
        :param Automata nfa: The automaton that state belongs to.
        :rtype set[AutomataNode]
    """

    reachableStates = set()     # Stores all states that can be reached via epsilon transition from this state.
    reachableStates.add(state)  # A state can always reach itself via epsilon transition.
    visitedStates.add(state)    # Visit this node so that further recursion doesn't re-add these transitions.

    # For each state reachable by epsilon transition that has not ben visited yet, calculate the epsilon closure
    # of that state and add it to the reachableStates set.
    if EPSILON in state.transitions:
        for nextState in state.transitions[EPSILON]:
            if nfa.nodes[nextState] not in visitedStates:
                reachableStates |= epsilonClosure(nfa.nodes[nextState], visitedStates, nfa)

    return reachableStates


def move(states, input):
    """ For a given set of states, returns all states reachable on a given input.

        :param list[AutomataNode] states: Set of states to transition from.
        :param str input: Input symbol over which to transition.
        :rtype: list[AutomataNode]
    """




if __name__ == "__main__":
    s0 = AutomataNode('s0')
    s1 = AutomataNode('s1')
    s2 = AutomataNode('s2')
    s3 = AutomataNode('s3')
    s4 = AutomataNode('s4')

    s0.addTransition('s1', EPSILON)
    s0.addTransition('s2', EPSILON)
    s1.addTransition('s3', EPSILON)
    s2.addTransition('s4', 'b')
    s3.addTransition('s4', 'a')

    testNFA = Automata()
    testNFA.addNodes([s0, s1, s2, s3, s4])

    print epsilonClosure(s0, set(), testNFA)
