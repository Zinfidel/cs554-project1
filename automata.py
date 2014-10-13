class Automata:
    """Represents a finite automaton."""

    def __init__(self, states=None, start="", accepts=None, transitions=None, alphabet=None):
        # Take care of default arguments - avoids issue of defaults being mutable/evaluated once.
        if states is None: states = []
        if accepts is None: accepts = []
        if transitions is None: transitions = []
        if alphabet is None: alphabet = []

        self.start = start
        """Starting state for this automata. This is the name of the node as a string."""

        self.accepts = accepts
        """List of names of accepting states for the automata. These are strings."""

        self.nodes = {name: AutomataNode(name) for name in states}
        """Dictionary of nodes in the automata. The key is the state name, the value is the node object."""

        self.alphabet = set(alphabet)
        """A set of symbols that comprise the alphabet for this automaton."""

        self.states = states
        """The states in raw, lexed form. This is necessary for some algorithms (Brzozowski)"""

        self.transitions = transitions
        """The transitions in raw, lexed form. This is necessary for some algorithms (Hopcroft's)"""

        # Set the accept state flag for all nodes in the accept list.
        for accState in accepts:
            self.nodes[accState].accept = True

        # Populate the nodes' transition dictionaries.
        for trans in transitions:
            fromState, symbols, toState = trans[0], trans[1], trans[2]
            for symbol in symbols:
                self.nodes[fromState].addTransition(toState, symbol)

    def __str__(self):
        ret = "Automaton:\n"
        ret += "Start:  " + self.start + '\n'
        ret += "Accept: " + str(self.accepts) + '\n'
        ret += "States: " + str([val.name for val in self.nodes.values()])
        return ret

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
    def __init__(self, name, accept=False):
        self.name = name
        """Name of this state. This should uniquely identify this state."""

        self.transitions = {}
        """Dictionary of symbol keys that returns lists of states."""

        self.accept = accept
        """Indicates that this node is an accept state."""

    def __str__(self):
        return self.name

    def __repr__(self):
        ret = "Node:   " + self.name + '\n'
        ret += "Accept: " + str(self.accept) + '\n'
        ret += "Transitions:\n"
        for key in self.transitions.keys():
            ret += "  " + key + " -> " + str([state for state in self.transitions[key]]) + '\n'

        return ret

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
