from automata import Automata
import description_reader

def revers(nfa):
    new_accept = []
    for s in nfa.start:
        new_accept.append(s)
    new_start = []
    for s in nfa.accepts:
        new_start.append(s)
    new_transitions = []
    for s in nfa.transitions:
        temp = s[0]
        s[0] = s[2]
        s[2] = temp
        new_transitions.append(s)
    return Automata(nfa.states, new_start, new_accept, new_transitions, nfa.alphabet)

def determinis(nfa):
#making all states
    new_states = []
    empty = []
    new_states.append(empty)
    for i in range(len(nfa.states)):
        for s in new_states:
            for i in range(len(nfa.states)):
                temp = []
                for x in s: temp.append(x)
                if nfa.states[i] not in temp:
                    temp.append(nfa.states[i])
                temp.sort()
                if temp not in new_states:
                    new_states.append(temp)

#making new start
    new_start = []
    temp = []
    for s in nfa.start:temp.append(s)
    temp.sort()
    new_start.append(temp)

#making new accept
    new_accept = []
    for s in new_states:
        is_accept = False
        for x in s:
            if x in nfa.accepts:
                is_accept = True
        if is_accept:new_accept.append(s)

#make new transitions
    new_transitions = []
    for from_state in new_states:
        for alpha in nfa.alphabet:
            to_state = []
            for s in from_state:
                #print "from_state : ",from_state," s : ",s," alpha : ",alpha
                terminal = nfa.nodes[s].getTransitionState(alpha)
                if not terminal == None:
                    for t in terminal:
                        if t not in to_state: to_state.append(t)
            #print "from_state: ",from_state, "alpha : ",alpha,"to_state : ",to_state
            to_state.sort()
            alphabet = []
            alphabet.append(alpha)
            new_t = []
            new_t.append(from_state)
            new_t.append(alphabet)
            new_t.append(to_state)
            new_transitions.append(new_t)
    #for x in new_transitions:print x
    #print new_transitions
    
    #change state names
    counter = 0
    for x in new_states:
        if x in new_start:
            new_start.remove(x)
            new_start.append(counter)
        if x in new_accept:
            new_accept.remove(x)
            new_accept.append(counter)
        for s in new_transitions:
            if s[0] == x:s[0] = counter
            if s[2] == x:s[2] = counter
        x = counter
        counter = counter + 1
    new_new_states = []
    for i in range(len(new_states)):new_new_states.append(i)
    #print new_new_states
    #print new_start
    #print new_accept
    #for x in new_transitions:print x
    return Automata(new_new_states, new_start, new_accept, new_transitions, nfa.alphabet)

def reachable(nfa):
    possible = []
    possible.append(nfa.start[0])
    next_state = []
    next_state.append(nfa.start[0])
    while not next_state == []:
        this_node = next_state[0]
        next_state.remove(this_node)
        for alpha in nfa.alphabet:
            for s in nfa.nodes[this_node].getTransitionState(alpha):
                if s not in possible:
                    possible.append(s)
                    if s not in next_state: next_state.append(s)
    possible.sort()
    new_accept = []
    for s in nfa.accepts:
        if s in possible: new_accept.append(s)
    new_transitions = []
    for x in nfa.transitions:
        if x[0] in possible and x[2] in possible:new_transitions.append(x)
    #print "all states: ",possible
    #print "stating point",nfa.start
    #print new_accept
    #for x in new_transitions: print x
    return Automata(possible, nfa.start, new_accept, new_transitions, nfa.alphabet)


def convertNfaToMinDfa(nfa):
    nfa = revers(nfa)
    nfa = determinis(nfa)
    nfa = reachable(nfa)
    nfa = revers(nfa)
    nfa = determinis(nfa)
    nfa = reachable(nfa)
    return nfa
