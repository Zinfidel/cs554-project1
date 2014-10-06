class Automata:
    """Represents a finite automaton."""

    def __init__(self, states=None, start="", accepts=None, transitions=None):
        # Take care of default arguments.
        if states is None: states = []
        if accepts is None: accepts = []
        if transitions is None: transitions = []

        self.start = start
        """Starting state for this automata. This is the name of the node as a string."""

        self.accepts = accepts
        """List of names of accepting states for the automata. These are strings."""

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
        """Name of this state. This should uniquely identify this state."""

        self.transitions = {}
        """Dictionary of symbol keys that returns lists of states."""

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
        # return str([(str(symbol) + " -> " + toState) for toState, symbol in self.transitions.items()])

    def __hash__(self):
        # Hash based entirely off of state name, as names *should* be unique.
        return hash(self.name)

    def __eq__(self, other):
        # Equality based entirely off of state name, as names *should* be unique.
        return self.name == other.name

    def getTransitionState(self, input_string):
        """Returns the state traversed to on a given input symbol, or none if no such transition exists."""
        if input_string in self.transitions:
            return self.transitions[input_string]
        else:
            return None

    def addTransition(self, toState, transSymbol):
        """Adds a transition to this state."""
        if transSymbol in self.transitions:
            self.transitions[transSymbol].append(toState)
        else:
            self.transitions[transSymbol] = [toState]
