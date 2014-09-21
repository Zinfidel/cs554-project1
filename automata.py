

class Automata:
    def __init__(self, startStates, acceptStates, nodelist):
        self.starts = startStates
        self.acceptStates = acceptStates
        self.nodes = nodelist

    def getStartStates():
        return self.starts

    def isAcceptState(state):
        return state in acceptStates

    def hasTransition(fromState, toState):
        return not (fromState.getTransition(to) is None)

class AutomataNode:
    def __inti__(self, nodeName, transitionDictionary):
        self.name = nodeName
        self.transitions = transitionDictionary

    def getTransition(state):
        if state in transitions:
            return transitions[state]
        else:
            return None
