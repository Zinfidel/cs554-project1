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
        :rtype: set[AutomataNode]
    """
    # Stores all states that can be reached via epsilon transition from this state.
    reachableStates = set()     
    # A state can always reach itself via epsilon transition.
    reachableStates.add(state)  
    # Visit this node so that further recursion doesn't re-add these transitions.
    visitedStates.add(state)    

    # For each state reachable by epsilon transition that has not ben visited yet,
    # calculate the epsilon closure of that state and add it to the 
    # reachableStates set.
    if EPSILON in state.transitions:
        for nextState in state.transitions[EPSILON]:
            if nfa.nodes[nextState] not in visitedStates:
                # Set data structure automatically discards duplicates.
                reachableStates |= epsilonClosure(nfa.nodes[nextState], \
                                                  visitedStates, nfa)

    return reachableStates


def move(states, symbol, nfa):
    """ For a given set of states, returns all states reachable on a given input.

        :param set[AutomataNode] states: Set of states to transition from.
        :param str symbol: Input symbol over which to transition.
        :param Automata nfa: The automaton that states belongs to.
        :rtype: set[AutomataNode]
    """

    reachableStates = set()

    for state in states:
        if symbol in state.transitions:
            # List comprehension so that we can get state objects back instead
            # of strings.
            reachableStates |= set([nfa.nodes[name] for name in \
                                    state.transitions[symbol]])

    return reachableStates


def convertNfaToDfa(nfa):
    """ Converts an NFA into a DFA via epsilon closure and subset construction.
        This code is based off of this pseudocode:

        =============================================================
        D-States = EpsilonClosure(NFA Start State) and it is unmarked
        while there are any unmarked states in D-States
        {
            mark T
            for each input symbol a
            {
                U = EpsilonClosure(Move(T, a));
                if U is not in D-States
                {
                    add U as an unmarked state to D-States
                }
            DTran[T,a] = U
            }
        }
        =============================================================

        :param Automata nfa: The non-deterministic finite automata to convert.
        :rtype: Automata
    """

    # The DFA being constructed.
    dfa = Automata()

    # Maps new state names to the collection of states they encompass. During the
    # construction of the new DFA, composite states such as {s0,s1,s2} can be
    # created, which is itself just one state, but needs to point to each of
    # the three states in the NFA it was constructed from.
    nameToStates = dict()

    # Sets to keep track of states that are waiting to be processed, and that
    # have been processed.
    markedStates = set()
    unmarkedStates = set()

    # Create initial DFA state from epsilon closure over NFA initial state.
    initStateClosure = epsilonClosure(nfa.nodes[nfa.start], set(), nfa)
    dfaInitState = AutomataNode(stateSetName(initStateClosure))

    # Add the initial composite state to the new DFA, the unmarked list, and 
    # the name map.
    dfa.addNodes([dfaInitState])
    dfa.start = dfaInitState.name
    unmarkedStates.add(dfaInitState)
    nameToStates[dfaInitState.name] = initStateClosure

    while unmarkedStates:
        # Mark the new state
        state = unmarkedStates.pop()
        markedStates.add(state)

        # Generate set of states from epsilon closures over every state returned
        # from this move.
        for symbol in nfa.alphabet:
            moveStates = move(nameToStates[state.name], symbol, nfa)

            # Only proceed if move produced states. Empty set means we don't 
            # bother with epsilon closures/new states.
            if moveStates:
                closureSet, visitedStates = set(), set()
                for moveState in moveStates:
                    closureSet |= epsilonClosure(moveState, visitedStates, nfa)

                # Generate new DFA state from combined epsilon closures.
                newDfaState = AutomataNode(stateSetName(closureSet))

                # If this new state is actually new, add new state to DFA, the 
                # unmarked list, and the name map.
                if (newDfaState not in unmarkedStates) and \
                   (newDfaState not in markedStates):
                    dfa.addNodes([newDfaState])
                    unmarkedStates.add(newDfaState)
                    nameToStates[newDfaState.name] = closureSet.copy()

                    # Add this node to the accept list if it is based off of an 
                    # accept node.
                    for node in closureSet:
                        if node.accept:
                            newDfaState.accept = True
                            dfa.accepts.append(newDfaState.name)
                            break

                # Add the transition to this (new) state.
                state.addTransition(newDfaState, symbol)

    return dfa


def stateSetName(states):
    """ Creates a name for a state derived from a supplied set of states. The 
        name is order-independent.
        
        :param set[AutomataNode] states: The states to derive a name from.
        :rtype: str
    """

    # Note: used list comprehension here instead of just printing list because 
    # list uses repr(), not str().

    # set(['c', 'b', 'a']) -> list['c', 'b', 'a']
    namesList = [str(item) for item in states]  
    # list['c', 'b', 'a']  -> ['a', 'b', 'c']
    namesList = str(sorted(namesList))          
    # ['a', 'b', 'c']      -> [a, b, c]
    namesList = namesList.replace('\'', '')     
    # [a, b, c]            -> [a,b,c]
    namesList = namesList.replace(' ', '')
    # [a,b,c]              -> a,b,c
    namesList = (namesList[1:])[:-1]           
    return namesList
