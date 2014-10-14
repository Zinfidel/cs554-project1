from description_reader import ConstructAutomata

def dfa_valid_string(automata, testing_string, current_state, current_step):
    if current_step == len(testing_string):
        for x in automata.accepts:
            if current_state == x: return True
        return False
    else:
        next_state = dfa.nodes[current_state].getTransitionState(testing_string[current_step])[0] # Only one state!
        if next_state is None: return False
        else: return dfa_valid_string(automata, testing_string, next_state, current_step + 1)
