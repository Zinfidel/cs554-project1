class enum.Automata_types:
    dfa = 1
    nfa = 2

class Automota:
    def __init__(self, type, states, start_state, accept_states):
        self.type = type
        self.states = states
        self.start_states = start_states
        self.accept_states = accept_states

    


class Node:
    transitions = {}
    def __init__(self, node_name, transitions):
        self.node_name = node_name
        self.transitions = transitions

    def transition(to):
        if transitions[to] is None:
            return None
        else:
            return transitions[to]
