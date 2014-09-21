

class Automata:
    def __init__(self, startStates, acceptStates, nodelist):
        self.starts = startStates
        self.acceptStates = acceptStates
        self.nodes = nodelist

    def getStartStates(self):
        return self.starts

    def isAcceptState(self, state):
        return state in acceptStates

    def hasTransition(self, fromState, toState):
        return not (fromState.getTransitions(to) is None)

class AutomataNode:
    def __init__(self, nodeName, transitionDictionary):
        self.name = nodeName
        self.transitions = transitionDictionary

    def getTransitions(self, state):
        if state in transitions:
            return transitions[state]
        else:
            return None



if __name__ == '__main__': 
    transitions= {'a':['b','c'], 'b':['a'], 'c':['a']}
    nodes = 'abc'
    a = Automata(['a'], ['b','c'], nodes)
    print a.hasTransition('a', 'b')
    
