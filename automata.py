class Automata:
    """Represents a finite automaton."""

    def __init__(self, states=None, start="", accepts=None, transitions=None):
        # Take care of default arguments.
        if states is None: states = []
        if accepts is None: accepts = []
        if transitions is None: transitions = []

        self.start = start
        """Starting state for this automata."""

        self.accepts = accepts
        """List of names of accepting states for the automata."""

        self.nodes = {name: AutomataNode(name) for name in states}
        """Dictionary of nodes in the automata. The key is the state name, the value is the node object."""

        # Populate the nodes' transition dictionaries.
        for trans in transitions:
            fromState, symbols, toState = trans[0], trans[1], trans[2]
            for symbol in symbols:
                self.nodes[fromState].addTransition(toState, symbol)

    def __str__(self):
        return "Start: " + str(self.start) \
               + " Accept: " + str(self.accepts) \
               + " States: " + str(self.nodes)

    def getAllStates(self):
        return self.nodes

    def getStartState(self):
        return self.start

    def isAcceptState(self, state):
        return state in self.accepts

    def hasTransition(self, fromState, toState):
        return not (self.nodes[fromState].getTransitions(toState) is None)

    def addNodes(self, nodes):
        """Adds supplied nodes (already constructed) to the automata. Expects a list."""
        for node in nodes:
            self.nodes[node.name] = node

class AutomataNode:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def __str__(self):
        # TODO: Not a very good representation of the node.
        return str([(str(symbol) + " -> " + toState) for toState, symbol in self.transitions.items()])

    def __repr__(self):
        return str(self)

    def getTransitionState(self, input_string):
        for state in self.transitions:
            for symbol in self.transitions[state]:
                if symbol == input_string: return state
        return None

    def addTransition(self, toState, transSymbol):

        if toState in self.transitions:
            self.transitions[toState].append(transSymbol)
        else:
            self.transitions[toState] = [transSymbol]
