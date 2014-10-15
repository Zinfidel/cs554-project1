from automata import Automata
from description_reader import ConstructAutomata


def hopcroftMinimize(dfa):
    P = [set(dfa.accepts),set(dfa.nodes.keys()).difference(set(dfa.accepts))]
    W = []
    if len(set(dfa.accepts)) > 1 : W.append(set(dfa.accepts))
    if len(set(dfa.nodes.keys()).difference(set(dfa.accepts))): \
           W.append(set(dfa.nodes.keys()).difference(set(dfa.accepts)))

    while len(W) != 0:
        A = W[0]
        W.remove(A)
        for c in dfa.alphabet:
            X = []
            for from_state in A:
                to_state = dfa.nodes[from_state].getTransitionState(c)
                # Only one possible state for DFAs!
                if to_state is not None: to_state = to_state[0]  
                if len(X) == 0 : X.append(from_state)
                else:
                    x_to_state = dfa.nodes[X[0]].getTransitionState(c)
                    for p in P:
                        if to_state in p and x_to_state[0] in p: X.append(from_state)
            if not len(X) == len(A):
                X1 = set(X)
                X2 = set(A).difference(X1)
                P.remove(set(A))
                P.append(X1)
                P.append(X2)
                if len(X1) > 1 : W.append(X1)
                if len(X2) > 1 : W.append(X2)
                break
    new_states = []
    for s in dfa.nodes.keys():
        new_states.append(s)
    new_accept = []
    for s in dfa.accepts:
        new_accept.append(s)
    new_transitions = []
    for s in dfa.transitions:
        new_transitions.append(s)

    for p in P:
        if len(p) > 1:
            this_state = None
            if dfa.start in p: this_state = dfa.start
            for current_state in p:
                if this_state == None: this_state = current_state
                elif not this_state == current_state:

                    if current_state in new_states:
                        new_states.remove(current_state)

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

    return Automata(new_states, dfa.start, new_accept, new_transitions,dfa.alphabet)
