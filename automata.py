class Automata:
    """Represents a finite automaton."""

    def __init__(self, states, starts, accepts, transitions,alphabet):
        self.starts = starts
        """List of names of starting states for the automata."""
        
        self.states = states
        """List of names of states for the automata."""

        self.accepts = accepts
        """List of names of accepting states for the automata."""
        
        self.alphabet = alphabet
        """List of names of accepting alphabet for the automata."""
        
        self.transitions = transitions
        """List of the transitions for the automata."""

        self.nodes = {name: AutomataNode(name) for name in states}
        """Dictionary of nodes in the automata. The key is the state name, the value is the node object."""

        # Populate the nodes' transition dictionaries.
        for trans in transitions:
            fromState, symbols, toState = trans[0], trans[1], trans[2]
            for symbol in symbols:
                self.nodes[fromState].addTransition(toState, symbol)

    def __str__(self):
        return "Start: " + str(self.starts)\
               + " Accept: " + str(self.accepts)\
               + " States: " + str(self.nodes)

    def getAllStates(self):
        return self.nodes

    def getStartStates(self):
        return self.starts

    def isAcceptState(self, state):
        return state in self.accepts

    def hasTransition(self, fromState, toState):
        return not (fromState.getTransitions(toState) is None)


class AutomataNode:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def __str__(self):
        # TODO: Not a very good representation of the node.
        return str([(str(symbol) + " -> " + toState) for toState, symbol in self.transitions.items()])

    def __repr__(self):
        return str(self)

    def getTransitions(self, state):
        if state in self.transitions:
            return self.transitions[state]
        else:
            return None

    def getTransitionState(self,input_string):
        for state in self.transitions:
            for symbol in self.transitions[state]:
                if (symbol == input_string): return state
        return None
                
    def addTransition(self, toState, transSymbol):
        if toState in self.transitions:
            self.transitions[toState].append(transSymbol)
        else:
            self.transitions[toState] = [transSymbol]
