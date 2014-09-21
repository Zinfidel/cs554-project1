

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
        return not (fromState.getTransitions(toState) is None)

class AutomataNode:
    def __init__(self, nodeName):
        self.name = nodeName
        self.transitions = {}

    def getTransitions(self, state):
        if state in self.transitions:
            return self.transitions[state]
        else:
            return None

    def addTransition(self, toState, transSymbol):
        self.transitions + {transSymbol:toState}



if __name__ == '__main__': 
    s1 = AutomataNode('s1')
    s2 = AutomataNode('s2')
    s3 = AutomataNode('s3')
    s1.addTransition(s2, 'a')
    nodes = [s1,s2,s3]
    a = Automata(s1, [s2,s3], nodes)
    print a.hasTransition(s1, s2)
    
