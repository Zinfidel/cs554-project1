from automata import Automata
import description_reader

dfa = description_reader.ConstructAutomata("testdata/dfa_x.txt")
P = [set(dfa.accepts),set(dfa.states).difference(set(dfa.accepts))]
W = []
if len(set(dfa.accepts)) > 1 : W.append(set(dfa.accepts))
if len(set(dfa.states).difference(set(dfa.accepts))): W.append(set(dfa.states).difference(set(dfa.accepts)))
#print "P is :",P
#print "W is :",W
while len(W) != 0:
    A = W[0]
    W.remove(A)
    for c in dfa.alphabet:
        X = []
        for from_state in A:
            to_state = dfa.nodes[from_state].getTransitionState(c)
            #print "from_state: ",from_state," using ",c," TO ",to_state
            if len(X) == 0 : X.append(from_state)
            else:
                x_to_state = dfa.nodes[X[0]].getTransitionState(c)
                for p in P:
                    if to_state in p and x_to_state in p: X.append(from_state)
        if not len(X) == len(A):
            X1 = set(X)
            X2 = set(A).difference(X1)
            P.remove(set(A))
            P.append(X1)
            P.append(X2)
            if len(X1) > 1 : W.append(X1)
            if len(X2) > 1 : W.append(X2)
                #print "------------------------------"
            break
new_states = []
for s in dfa.states:
    new_states.append(s)
new_accept = []
for s in dfa.accepts:
    new_accept.append(s)
new_transitions = []
for s in dfa.transitions:
    new_transitions.append(s)

#print dfa
#print P

for p in P:
    if len(p) > 1:
        this_state = None
        if dfa.starts in p: this_state = dfa.starts
        for current_state in p:
            if this_state == None: this_state = current_state
            elif not this_state == current_state:
                #print new_states
                #print current_state
                if current_state in new_states:
                    new_states.remove(current_state)
                #print new_states
                if current_state in new_accept:
                    new_accept.remove(current_state)
                    new_accept.append(this_state)
                remove_transitions = []
                for transition in new_transitions:
                    if transition[0] == current_state:
                        remove_transitions.append(transition)
                    elif transition[2] == current_state:
                        transition[2] = this_state
                for p in remove_transitions:
                    new_transitions.remove(p)

new_dfa = Automata(new_states, dfa.starts, new_accept, new_transitions,dfa.alphabet)
print new_dfa
#print new_states
#print new_accept
#for p in new_transitions:
#    print p